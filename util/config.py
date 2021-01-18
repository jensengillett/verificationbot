import os.path as osp
import toml


class BotConfig:

    def __init__(self, config_path):
        self.config_path = config_path
        self.def_config = {
            'bot': {
                'token': 'bot.token',
                'key': '$',
                'used_emails': 'used_emails.txt',
                'warn_emails': 'exchange_emails.txt',
                'moderator_email': 'discordauthentemail@gmail.com'
            },
            'email': {
                'sample': 'accountid',
                'domain': 'gmail.com',
                'from': 'example@gmail.com',
                'password': 'password',
                'subject': 'Verification',
                'server': 'smtp.gmail.com',
                'port': '465'
            },
            'discord': {
                'server_role': 'email_verify',
                'channel_id': 12341234123412,
                'notify_id': 12341234123412,
                'admin_id': 12341234123412,
                'author_name': 'User'
            }
        }

        self.data = self.load_data()
        self.do_run = True

    def load_data(self):
        if osp.isfile(self.config_path):
            with open(self.config_path, 'r') as file:
                data = toml.load(file)
                # Logger.info("Config loaded.")
                return data

        else:
            with open(self.config_path, 'w') as file:
                print("Config file not found, creating...")
                toml.dump(self.def_config, file)
                print("Config file created")
                self.do_run = False
                raise Exception("Config created, needs to be filled.")