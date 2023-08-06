from google.protobuf.json_format import ParseDict
from os import EX_OK, EX_SOFTWARE, EX_DATAERR, EX_NOINPUT, getenv
from pathlib import Path
import json
import jwt
import requests
import sys


class InstanceError(Exception):
    pass


def value_from_id_token(id_token, key):
    data = jwt.decode(id_token, options={"verify_signature": False})
    if not key in data:
        raise InstanceError("while decoding id token")
    else:
        return data[key]


def get_config():
    config = Path(Path.home(), ".sabana", "config.json")
    if not config.is_file():
        raise InstanceError("are you logged in?, use <sabana login>")
    with open(config, "r") as f:
        return json.load(f)


def get_access_token(config):
    if not "access_token" in config:
        raise InstanceError("access token not found in config file")
    else:
        return config["access_token"]


def get_id_token(config):
    if not "access_token" in config:
        raise InstanceError("id token not found in config file")
    else:
        return config["id_token"]


def post(url, token, request):
    response = requests.post(
        url,
        data=json.dumps(request),
        headers={
            "Content-Type": "application/json",
            "Authorization": token,
        },
    )
    if response.status_code == 400:
        print(response.json())
        raise DeviceError("Returned error 400, check your request arguments")
    elif response.status_code == 500:
        print(response.json())
        raise DeviceError(
            "Returned error 500, there was an error on the Sabana platform."
        )
    else:
        return response.json()


class Instance:
    """
    Instance: handler for an instance in the Sabana platform.

              Can be created either by specifying user, instance, tag
              or by providing a URL.
    """

    __ENDPOINT = "https://deploy.sabana.io"

    def __init__(self, user=None, instance=None, tag=None, url=None):
        try:
            config = get_config()
            self.access_token = get_access_token(config)
            self.id_token = get_id_token(config)
        except InstanceError:
            self.access_token = getenv("SABANA_ACCESS_TOKEN")
            self.id_token = getenv("SABANA_ID_TOKEN")
            if not isinstance(self.access_token, str) or not isinstance(
                self.id_token, str
            ):
                print("ERROR: Could not find credentials on local file or environment.")
                print(
                    "       Use the following command to log-in using the Sabana CLI:\n"
                )
                print("sabana login\n")
                print("Alternatively setup the following environment variables:")
                print("SABANA_ACCESS_TOKEN, SABANA_ID_TOKEN")
                sys.exit(EX_SOFTWARE)
        except Exception as e:
            print("Fatal error trying to get credentials by the Instance object.")
            print("Contact Sabana for support.")
            sys.exit(EX_SOFTWARE)

        if all(not i is None for i in (user, instance, tag)) and url is None:
            pass
        elif all(i is None for i in (user, instance, tag)) and not url is None:
            pass
        else:
            raise InstanceError("Define user, instance, and tag, or a url")

        self.instance_url = url
        self.user = user
        self.instance = instance
        self.tag = tag
        self.is_up = False

    def __str__(self) -> str:
        msg = "Sabana Instance:\n"
        if all(isinstance(i, str) for i in (self.user, self.instance, self.tag)):
            msg += f"Instance: {self.user}/{self.instance}:{self.tag}\n"
        if isinstance(self.instance_url, str):
            msg += f"Deployed at: {self.instance_url}"
        return msg

    def __del__(self):
        try:
            isup = self.is_up
        except AttributeError:
            # If the user tries to create an object with wrong arguments
            # this function will be called without self.is_up being defined.
            pass
        else:
            if self.is_up:
                self.down()

    def up(self):
        url = "{}/api/v0/up".format(self.__ENDPOINT)
        req = {
            "user": self.user,
            "instance": self.instance,
            "tag": self.tag,
        }
        try:
            res = post(url, self.access_token, req)
        except Exception as e:
            raise InstanceError("Failed bringing instance up: {}".format(e))
        else:
            if not "url" in res:
                print("Error: up was not successful. Have you logged in?")
                print("       to login use the Sabana CLI: sabana login")
                raise InstanceError("not able to up that instance")
            if len(res["url"]) == 0:
                raise InstanceError("Got invalid URL from server.")
            else:
                self.instance_url = res["url"]
                self.is_up = True
                print(
                    "Instance {}/{}:{} is up".format(self.user, self.instance, self.tag)
                )
                print(self.instance_url)

    def down(self):
        url = "{}/api/v0/down".format(self.__ENDPOINT)
        req = {
            "url": self.instance_url,
        }
        try:
            res = post(url, self.access_token, req)
        except Exception as e:
            raise InstanceError(
                "Failed bringing {}/{}:{} down: {}".format(
                    self.user, self.instance, self.tag, str(e)
                )
            )
        else:
            print(
                "Instance {}/{}:{} is down".format(self.user, self.instance, self.tag)
            )
            self.is_up = False
            self.instance_url == ""
