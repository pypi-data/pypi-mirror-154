from os import access
from typing import Optional
from aiohttp import ClientSession, ClientResponseError

from .const import (
    CENTRO_BASE_URL,
    CENTRO_DEVICE_TYPE,
    CENTRO_DEVICE_TYPES,
    CENTRO_EMAIL,
    CENTRO_LOGIN_URL,
    CENTRO_PASSWORD,
    CENTRO_SETWORKMODE_URL,
    HTTP_GET,
    HTTP_POST,
    CENTRO_DEVICELIST_URL,
    CENTRO_DEVICESETTINGS_URL,
    CENTRO_USER,
    CENTRO_ACCESS_TOKEN,
    CENTRO_DEVICE
)

from .device import ESICentroDevice
from .responses import ESICentroLoginResponse, SetThermostatTempResponse
from .responses import RequestThermostatIDsResponse
from .responses import RequestThermostatDataResponse
from .utilities import Utilities

import logging
logger = logging.getLogger(__name__)

class ESICentroClient:
    """[summary]"""

    __slots__ = [
        "_email",
        "_password",
        "_user_id",
        "_access_token",
        "_session_details",
        "_device_ids",
    ]

    def __init__(
        self, email, password, session_details, user_id=None, access_token=None
    ):

        if session_details is not None:
            self.session_details = session_details
        else:
            self.session_details = ClientSession()

        self.user_id = user_id
        self.password = password
        self.email = email
        self.access_token = access_token

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        self._user_id = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value

    @property
    def access_token(self):
        return self._access_token

    @access_token.setter
    def access_token(self, value):
        self._access_token = value

    @property
    def session_details(self):
        return self._session_details

    @session_details.setter
    def session_details(self, value):
        self._session_details = value

    @property
    def device_ids(self):
        return self._device_ids

    @device_ids.setter
    def device_ids(self, value):
        self._device_ids = value

    async def login(self, timeout=5):
        response = await Utilities.make_http_request(
            self.session_details,
            HTTP_POST,
            CENTRO_BASE_URL + CENTRO_LOGIN_URL,
            params={
                CENTRO_EMAIL: self.email,
                CENTRO_PASSWORD: self.password,
            },
            timeout=timeout,
        )

        authorize_response = await Utilities.process_http_response(
            response, ESICentroLoginResponse
        )

        self.user_id = authorize_response.user_id
        self.access_token = authorize_response.access_token

        return authorize_response

    async def request_thermostat_ids(self, timeout=5):
        response = await Utilities.make_http_request(
            self.session_details,
            HTTP_GET,
            CENTRO_BASE_URL + CENTRO_DEVICELIST_URL,
            params={
                CENTRO_DEVICE_TYPE: CENTRO_DEVICE_TYPES,
                CENTRO_USER: self.user_id,
                CENTRO_ACCESS_TOKEN: self.access_token,
            },
            timeout=timeout,
        )

        processed_response = await Utilities.process_http_response(
            response, RequestThermostatIDsResponse
        )

        self.device_ids = processed_response.device_ids

        return processed_response

    async def request_thermostat_data(self, device_id, timeout=5):
        response = await Utilities.make_http_request(
            self._session_details,
            HTTP_GET,
            CENTRO_BASE_URL + CENTRO_DEVICESETTINGS_URL,
            params={
                CENTRO_DEVICE: device_id,
                CENTRO_USER: self.user_id,
                CENTRO_ACCESS_TOKEN: self.access_token,
            },
            timeout=timeout,
        )

        processed_response = await Utilities.process_http_response(
            response, RequestThermostatDataResponse
        )

        return processed_response

    async def set_thermostat_temperature(
        self, device_id, current_temprature, work_mode, timeout=5
    ):
        messageId = await Utilities.randomMsgId()
        current_temperature = Utilities.convert_to_esi_temp(current_temprature)
        response = await Utilities.make_http_request(
            self.session_details,
            HTTP_POST,
            CENTRO_BASE_URL + CENTRO_SETWORKMODE_URL,
            params={
                CENTRO_DEVICE: device_id,
                "current_temprature": current_temperature,
                CENTRO_USER: self.user_id,
                CENTRO_ACCESS_TOKEN: self.access_token,
                "work_mode": work_mode,
                "messageId": messageId,
            },
            timeout=timeout,
        )

        processed_response = await Utilities.process_http_response(
            response, SetThermostatTempResponse
        )

        return processed_response
