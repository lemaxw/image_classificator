from clarifai_grpc.grpc.api import service_pb2, resources_pb2
from clarifai_grpc.grpc.api.status import status_code_pb2
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import service_pb2_grpc

import grpc
import sys

def get_tags_clarifai(image_path):

    with open(image_path, "rb") as f:
        file_bytes = f.read()

    stub = service_pb2_grpc.V2Stub(ClarifaiChannel.get_grpc_channel())

    request = service_pb2.PostModelOutputsRequest(
        # This is the model ID of a publicly available General model. You may use any other public or custom model ID.
        model_id="general-image-recognition",
        user_app_id=resources_pb2.UserAppIDSet(app_id="get_tags"),
        inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        image=resources_pb2.Image(base64=file_bytes)
                    )
                )
            ]
    )

    metadata=(
            ("authorization", "Key 820fa297eb6d4c739fe183cce4956e18"),
        )


    response = stub.PostModelOutputs(request, metadata=metadata)

    if response.status.code != status_code_pb2.SUCCESS:
        raise Exception(
            "Post model outputs failed, status: "
            + response.status.description
        )

    res_hash = {};
    # Extract and print the results
    for concept in response.outputs[0].data.concepts:
        res_hash[concept.name]=concept.value
    return res_hash
    
