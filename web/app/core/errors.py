from fastapi.exceptions import HTTPException
from fastapi import status


HTTP404_NOTFOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Not Found"
)

HTTP400_BADREQUEST = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Not Found"
)

HTTP500_INTERNALERROR = HTTPException(
    status_code=status.HTTP500_INTERNALERROR,
    detail="Internal Error"
)
