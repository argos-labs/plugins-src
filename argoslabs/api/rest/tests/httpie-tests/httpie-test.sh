#!/usr/bin/env bash

## https://docs.microsoft.com/en-us/azure/cognitive-services/face/quickstarts/curl
SUBSCRIPTION_KEY="034f8bfbcad0435c8bad047980d8d811"
http POST "https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect?returnFaceId=true&returnFaceLandmarks=false&returnFaceAttributes=age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise" \
"Ocp-Apim-Subscription-Key: ${SUBSCRIPTION_KEY}" \
"Content-Type:application/json" \
url=https://upload.wikimedia.org/wikipedia/commons/c/c3/RH_Louise_Lillian_Gish.jpg

# https://console.bluemix.net/docs/services/visual-recognition/getting-started.html#-
IBM_KEY="QEhZ-LvhDkhNrVrXa-hNtFQz_8QK4fsCrsojIF8vpKbt"
#curl -X POST --form "images_file=@fruitbowl.jpg" -u "apikey:${IBM_KEY}" "https://gateway.watsonplatform.net/visual-recognition/api/v3/classify?version=2016-05-20"
http --form --auth apikey:${IBM_KEY}  POST "https://gateway.watsonplatform.net/visual-recognition/api/v3/classify?version=2016-05-20" images_file@fruitbowl.jpg
http --form --auth apikey:${IBM_KEY}  POST "https://gateway.watsonplatform.net/visual-recognition/api/v3/detect_faces?version=2016-05-20" images_file@prez.jpg






