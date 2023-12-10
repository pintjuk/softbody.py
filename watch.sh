pipenv fmt 
pipenv lint
pipenv run run &
FOO_PID=$!
# do other stuff
fswatch -0 main.py | while read -d "" event 
do 
    echo event:${event}
	kill $FOO_PID
	pipenv fmt 
	pipenv lint
	pipenv run run &
	FOO_PID=$!
done
