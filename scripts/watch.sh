pipenv run run &
FOO_PID=$!
# do other stuff
fswatch -0 src | while read -d "" event 
do 
    echo event:${event}
	kill $FOO_PID
	pipenv run run &
	FOO_PID=$!
done
