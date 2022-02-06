import requests

from lib.file_handler import ExcelFileHandler, FileHandlerChain
from lib.file_io import EnvironmentFileIOFactory
from lib.responder import AddressValidationResponder, CarrierRouteRetreiverResponder, ReportGeneratorResponder, ResponderPipeline



default_file_handler_chain = FileHandlerChain()
default_file_handler_chain.add_handler(ExcelFileHandler())

default_responder_pipeline = ResponderPipeline()
default_responder_pipeline.add_last(AddressValidationResponder(requests))
default_responder_pipeline.add_last(CarrierRouteRetreiverResponder(requests))
default_responder_pipeline.add_last(ReportGeneratorResponder())