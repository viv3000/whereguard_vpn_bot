import logging

def logInfo(message: str, tg_user):
    if (tg_user.username == None):
        logging.info(f'user_id: {tg_user.id}; message: {message}')
    else:
        logging.info(f'user_name: {tg_user.username}; message: {message}')


def logError(message: str, tg_user):
    if (tg_user.username == None):
        logging.error(f'user_id: {tg_user.id}; message: {message}', exc_info=True)
    else:
        logging.error(f'user_name: {tg_user.username}; message: {message}', exc_info=True)
