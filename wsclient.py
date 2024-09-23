import lark_oapi as lark
from config import Settings

settings = Settings()

def do_p2_im_message_receive_v1(data: lark.im.v1.P2ImMessageReceiveV1) -> None:
    print(f'[ do_p2_im_message_receive_v1 access ], data: {lark.JSON.marshal(data, indent=4)}')


def do_message_event(data: lark.CustomizedEvent) -> None:
    print(f'[ do_customized_event access ], type: message, data: {lark.JSON.marshal(data, indent=4)}')


event_handler = lark.EventDispatcherHandler.builder("", "") \
    .register_p2_im_message_receive_v1(do_p2_im_message_receive_v1) \
    .register_p1_customized_event("这里填入你要自定义订阅的 event 的 key,例如 out_approval", do_message_event) \
    .build()


def main():
    cli = lark.ws.Client(settings.lark_id, settings.lark_secret,
                         event_handler=event_handler, log_level=lark.LogLevel.DEBUG)
    cli.start()


if __name__ == "__main__":
    main()