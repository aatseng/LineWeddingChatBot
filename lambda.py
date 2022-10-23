import json
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (LineBotApiError, InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage, SourceUser, SourceGroup, SourceRoom, TemplateSendMessage, ConfirmTemplate, MessageAction, ButtonsTemplate, 
    ImageCarouselTemplate, ImageCarouselColumn, URIAction, PostbackAction, DatetimePickerAction, CameraAction, CameraRollAction, LocationAction, CarouselTemplate, CarouselColumn, 
    PostbackEvent, StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage, ImageMessage, VideoMessage, AudioMessage, FileMessage, UnfollowEvent, FollowEvent, 
    JoinEvent, LeaveEvent, BeaconEvent, MemberJoinedEvent, MemberLeftEvent, FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent, TextComponent, SpacerComponent, 
    IconComponent, ButtonComponent, SeparatorComponent, QuickReply, QuickReplyButton, ImageSendMessage)
import requests, traceback, logging, boto3, json, sys, os
from botocore.exceptions import ClientError
from bs4 import BeautifulSoup
from linebot.models.flex_message import (
    BubbleContainer, ImageComponent
)
from linebot.models.actions import URIAction

logger = logging.getLogger()
logger.setLevel(logging.INFO) 
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if not channel_secret or not channel_access_token:
    logger.error('Need to setup LINE_CHANNEL_SECRET and LINE_CHANNEL_ACCESS_TOKEN in os enviorment')
    sys.exit(1)
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)    
logger.info(os.environ)  

def get_userOperations(userId):
    return None

def compose_textReplyMessage(userId, userOperations, messageText):
    if  messageText == '日期':
        return TextSendMessage(text='2023/01/08')
    elif  messageText == '幾號':
        return TextSendMessage(text='2023/01/08')
    elif messageText == '地址':
        return TextSendMessage(text='https://g.page/TheHistoricalGrandCourtyard?share')
    return TextSendMessage(text='Getting: %s!' % messageText)

def compose_postbackReplyMessage(userId, userOperations, messageData):
    return TextSendMessage(text='好的！已收到您的動作 %s！' % messageData)

def lambda_handler(event, context):
    
    @handler.add(MessageEvent, message=TextMessage)    
    def handle_text_message(event):
        userId = event.source.user_id
        messageText = event.message.text
        userOperations = get_userOperations(userId)
        logger.info('User [%s] saying [%s]' % (userId, messageText))
        if messageText == 'aaa':
            flex_message = FlexSendMessage(
                alt_text='hello',
                 contents={ }
            )
line_bot_api.reply_message(event.reply_token, flex_message)
        line_bot_api.reply_message(event.reply_token, compose_textReplyMessage(userId, userOperations, messageText))

    @handler.add(PostbackEvent)   
    def handle_postback(event):
        userId = event.source.user_id 
        messageData = json.loads(event.postback.data)
        userOperations = get_userOperations(userId)        
        logger.info('Getting PostbackEvent | user %s' % userId)        
        line_bot_api.reply_message(event.reply_token, compose_postbackReplyMessage(userId, userOperations, messageData))

    @handler.add(FollowEvent)  
    def handle_follow(event):
        userId = event.source.user_id
        logger.info('Getting event | user %s' % userId)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='Hi 你好!'))      

    try:
        signature = event['headers']['x-line-signature']  
        body = event['body']  
        handler.handle(body, signature)  # 
    
    except InvalidSignatureError:
        return {
            'statusCode': 400,
            'body': json.dumps('InvalidSignature') }        
    
=    except LineBotApiError as e:
        logger.error('Calling LINE API Error: %s' % e.message)
        for m in e.error.details:
            logger.error('-- %s: %s' % (m.property, m.message))
        return {
            'statusCode': 400,
            'body': json.dumps(traceback.format_exc()) }
    
    return {
        'statusCode': 200,
        'body': json.dumps('OK') }