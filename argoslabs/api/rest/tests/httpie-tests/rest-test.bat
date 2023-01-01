REM ECHO OFF
REM ## https://docs.microsoft.com/en-us/azure/cognitive-services/face/quickstarts/curl
set SUBSCRIPTION_KEY=034f8bfbcad0435c8bad047980d8d811

REM http POST "https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect?returnFaceId=true&returnFaceLandmarks=false&returnFaceAttributes=age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise"^
REM 	"Ocp-Apim-Subscription-Key: %SUBSCRIPTION_KEY%"^
REM 	"Content-Type:application/json"^
REM 	"url=https://upload.wikimedia.org/wikipedia/commons/c/c3/RH_Louise_Lillian_Gish.jpg"
argoslabs.api.rest^
	--req-item "Ocp-Apim-Subscription-Key: %SUBSCRIPTION_KEY%"^
	--req-item "Content-Type:application/json"^
	--req-item "url=https://upload.wikimedia.org/wikipedia/commons/c/c3/RH_Louise_Lillian_Gish.jpg"^
	post^
	"https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect?returnFaceId=true&returnFaceLandmarks=false&returnFaceAttributes=age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise"
	

REM # https://console.bluemix.net/docs/services/visual-recognition/getting-started.html#-
set IBM_KEY=QEhZ-LvhDkhNrVrXa-hNtFQz_8QK4fsCrsojIF8vpKbt
REM #curl -X POST --form "images_file=@fruitbowl.jpg" -u "apikey:${IBM_KEY}" "https://gateway.watsonplatform.net/visual-recognition/api/v3/classify?version=2016-05-20"

REM http --form --auth apikey:%IBM_KEY%  POST "https://gateway.watsonplatform.net/visual-recognition/api/v3/classify?version=2016-05-20" images_file@fruitbowl.jpg
argoslabs.api.rest^
	--form^
	--auth apikey:%IBM_KEY%^
	--req-item images_file@fruitbowl.jpg^
	post^
	"https://gateway.watsonplatform.net/visual-recognition/api/v3/classify?version=2016-05-20"

REM http --form --auth apikey:%IBM_KEY%  POST "https://gateway.watsonplatform.net/visual-recognition/api/v3/detect_faces?version=2016-05-20" images_file@prez.jpg
argoslabs.api.rest^
	--form^
	--auth apikey:%IBM_KEY%^
	--file prez.jpg^
	--req-item images_file@@1^
	POST^
	"https://gateway.watsonplatform.net/visual-recognition/api/v3/detect_faces?version=2016-05-20"

