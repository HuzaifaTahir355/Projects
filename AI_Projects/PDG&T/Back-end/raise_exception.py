from fastapi import HTTPException, status

class RaiseException:
    def data_extraction_error(e):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail=f"Error While loading data - \n {e}")
    
    def invalid_file_format():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Format is not Supported")
    
    def env_var_not_found(e):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Missing API key - \n {e}")
    

