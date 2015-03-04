from datetime import datetime
import gevent
import lymph


class Hi(lymph.Interface):

    def apply_config(self, config):
        super(Hi, self).apply_config(config)
        self.username = config.root.get('username')

    def on_start(self):
        super(Hi, self).on_start()
        self.emit('hi.joined', {'username': self.username, 'timestamp': str(datetime.now())})

    @lymph.event('hi.message')
    def receive_message(self, event):
        print('({timestamp}) {username}: {message}'.format(**event.body))

    @lymph.event('hi.joined')
    def user_joined(self, event):
        print('({timestamp}) {username} joined.'.format(**event.body))


class HiClient(lymph.Interface):

    def apply_config(self, config):
        super(HiClient, self).apply_config(config)
        self.username = config.root.get('username')

    def on_start(self):
        super(HiClient, self).on_start()
        gevent.spawn(self._chat_repl)

    def _chat_repl(self):
        while True:
            user_input = raw_input('> ')
            if user_input == ':quit':
                return
            else:
                self._send(user_input)

    def _send(self, message):
        self.emit('hi.message', {'message': message, 'username': self.username, 'timestamp': str(datetime.now())})


class HiBot(lymph.Interface):

    def on_start(self):
        super(HiBot, self).on_start()
        self.talking = gevent.spawn(self.talk_forever)

    def talk_forever(self):
        while True:
            self.emit('hi.message', {'message': "Hi, it's HiBot :)", 'username': 'HiBot', 'timestamp': str(datetime.now())})
            gevent.sleep(3)

    def on_stop(self, *args, **kwargs):
        super(HiBot, self).on_stop(*args, **kwargs)
        self.talking.kill()
