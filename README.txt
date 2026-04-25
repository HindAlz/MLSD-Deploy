curl https://flask-model-api-42666501068.us-central1.run.app/health

curl -X POST https://flask-model-api-42666501068.us-central1.run.app/predict -H "Content-Type: application/json" -d '{"features":{"profile pic":0,"name==username":0,"external URL":0,"private":0,"followers":50,"follows":300,"posts":5,"description length":10,"username length":15,"fullname length":12}}'