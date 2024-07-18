import json
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from myWhisper.models import ChatMessage, Thread

User = get_user_model()


# extends asyncconsumer
class WhisperConsumer(AsyncConsumer):

    # async: diğer görevler durdurulmadan methodun gerçekleştirilmesini sağlar
    # print("", event): line output the 'event' to console or logs
    async def websocket_connect(self, event):
        print("connected", event)

        # retrive the connected user from the scope
        # scope is a dictionary-like object contain info about the connection
        # authentication middleware add the user to the scope
        user = self.scope['user']

        # based on user_id create chatroom name
        # f-string in Pytho allows embedding expressions inside string literals
        chat_room = f'user_chatroom_{user.id}'
        # assign chat room name to an instance variable
        # so it can be accessible from other methods
        self.chat_room = chat_room

        # await: call async function and wait for it to complete
        # adds the current WS connection (self.channel_name) to a group (chat_room)
        # channel_layer is an interface to the Django Channel's backend
        await self.channel_layer.group_add(
            chat_room,
            self.channel_name,
        )

        # await: async
        # self.send: send a message back to the client over the WS connection
        await self.send({
            # accept connection, without this WS connection closed by default
            'type': 'websocket.accept',
        })

    # async : define async function
    # self: whisper consumer class
    # event: the object containing details about the WS message
    async def websocket_receive(self, event):
        print("received", event)

        # parse the received JSON string into a Python dictionary
        received_data = json.loads(event['text'])

        # extract the values associated with the keys from JS
        msg = received_data.get('message')
        sent_by_id = received_data.get('sent_by')
        send_to_id = received_data.get('send_to')
        thread_id = received_data.get('thread_id')

        # check if the message is missing or empty
        if not msg:
            print('Error: message error')
            return False

        # take asyncly user object using get_user_object and get_thread methods
        # these methods written in this doc.
        sent_by_user = await self.get_user_object(sent_by_id)
        send_to_user = await self.get_user_object(send_to_id)
        thread_obj = await self.get_thread(thread_id)

        # check anyone is missing
        if not send_to_user or not sent_by_user or not thread_id:
            print('Error: user or thread error')

        # asyncly create new chat message in the database
        await self.create_chat_messages(thread_obj, sent_by_user, msg)

        # create chat room name for the recipient user using their ID
        other_user_chat_room = f'user_chatroom_{send_to_id}'

        # retrive the current user from the scope
        # scope is a dictionary-like object contain info about the connection
        # authentication middleware add the user to the scope
        self_user = self.scope['user']
        # prepare the response dictionary to be sent back to the WS clients
        response = {
            'message': msg,
            'sent_by': self_user.id,
            'thread_id': thread_id
        }

        # RECIPIENT CHAT ROOM
        # asyncly send a message to the specified group
        # use the created response for
        await self.channel_layer.group_send(
            # name of the recipient chat room
            other_user_chat_room,
            {
                # chat message + json encoded response
                'type': 'chat_message',
                'text': json.dumps(response)
            }
        )

        # To apply P2P communication (without sending to server)
        # Should use WebRTC

        # SENDERS CHAT ROOM
        # ascycnly send a message to the current user's chat room
        await self.channel_layer.group_send(
            # the name of the current user's chat room
            self.chat_room,
            {
                'type': 'chat_message',
                'text': json.dumps(response)
            }
        )

    # connection is closed, this method is triggered automatically when
    # the connection btw the client and server is terminated
    async def websocket_disconnect(self, event):
        print("disconnected", event)

        # Remove the user from the chat room group
        await self.channel_layer.group_discard(
            self.chat_room,
            self.channel_name,
        )

    # handle incoming chat messages that sent to WS channel
    async def chat_message(self, event):
        print("chat_message", event)
        # self.send: send method of the customer
        # responsible for sending data back to the WS client
        await self.send({
            'type': 'websocket.send',
            'text': event['text']
        })

    # Decorator: converts a sync fonc into an async one.
    # It allows the func to be called in async context
    # while ensuring that db access (sync) is handled properly
    @database_sync_to_async
    def get_user_object(self, user_id):
        # create query set
        qs = User.objects.filter(id=user_id)

        # check the instance
        if qs.exists():
            obj = qs.first()
        else:
            obj = None
        return obj

    # Decorator: Access control, caching, middleware functionalities
    # it helps keep the code clean and maintainable
    @database_sync_to_async
    def get_thread(self, thread_id):
        qs = Thread.objects.filter(id=thread_id)
        if qs.exists():
            obj = qs.first()
        else:
            obj = None
        return obj

    # create new message obj and save the new message to the db immediately
    @database_sync_to_async
    def create_chat_messages(self, thread, user, msg):
        qs = ChatMessage.objects.create(thread=thread, user=user, message=msg)
