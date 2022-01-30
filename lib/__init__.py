import requests

from lib.file_handler import ExcelFileHandler, FileHandlerChain
from lib.responder import AddressValidationResponder, CarrierRouteRetreiverResponder, ResponderPipeline


default_file_handler_chain = FileHandlerChain()
default_file_handler_chain.add_handler(ExcelFileHandler())

default_responder_pipeline = ResponderPipeline()
default_responder_pipeline.add_last(AddressValidationResponder(requests))
default_responder_pipeline.add_last(CarrierRouteRetreiverResponder(requests))