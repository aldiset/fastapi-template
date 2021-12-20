from contextlib import contextmanager

from sqlalchemy.exc import NoResultFound, IntegrityError

from app.src.utils.response_builder import ResponseBuilder, ResponseListBuilder
from fastapi import status
from app.src.exception.auth import UnauthorizedError
from app.src.core.logger import logger
import sqlalchemy
import traceback


@contextmanager
def api_exception_handler(res, response_type=None):
    response = ResponseListBuilder() if response_type == 'list' else ResponseBuilder()
    try:
        yield response

    except ValueError as error:
        res.status_code = status.HTTP_400_BAD_REQUEST
        response.status = False
        response.code = res.status_code
        response.message = str(error)

    except IntegrityError as error:
        res.status_code = status.HTTP_400_BAD_REQUEST
        response.status = False
        response.code = res.status_code
        response.message = str(error.__dict__['orig'])

    except FileNotFoundError as error:
        res.status_code = status.HTTP_404_NOT_FOUND
        response.status = False
        response.code = res.status_code
        response.message = str(error) if str(error) else "Data tidak ditemukan"

    except UnauthorizedError as error:
        res.status_code = status.HTTP_401_UNAUTHORIZED
        response.status = False
        response.code = res.status_code
        response.message = str(error)
    
    except Exception as error:
        traceback.print_exc()
        logger.warning(traceback.format_exc())
        res.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        response.status = False
        response.code = res.status_code
        response.message = str(error)
