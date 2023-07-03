import functions_framework
from transfer import transfer

@functions_framework.http
def transfer_data(request):

    request_json = request.get_json(silent=True)
    transfer()

    return "Data has already transfered!"