#!/bin/bash

source bin/activate

for i in 1 {1..75}
do
	./getart.sh

	./dharma.py
done

deactivate

exit 0
