# sigo-uploader-api
Micro serviço em Lambda responsável por realizar upload de arquivos para o S3 .
Faz parte do nosso TCC do curso Especialização em Arquitetura de Software Distribuído da PUC Minas.

[comment]: <> (<!-- badges -->)

[comment]: <> ([![Open Source Love]&#40;https://badges.frapsoft.com/os/mit/mit.svg?v=102&#41;]&#40;&#41;)

[comment]: <> (## Prerequisites)

[comment]: <> (- Python 3.6)

[comment]: <> (- Chalice)

[comment]: <> (- python-dotenv)

[comment]: <> (- pytz)

[comment]: <> (## Features)

[comment]: <> (- Docker-compose )

[comment]: <> (- Chalice  )

[comment]: <> (## Installation)

[comment]: <> (Follow the next steps)

[comment]: <> (### Running Locally)

[comment]: <> (You will need the aws credentials for the profile `sigo-lambdas`:)

[comment]: <> (```)

[comment]: <> (cat ~/.aws/credentials)

[comment]: <> ([sigo-lambdas])

[comment]: <> (aws_access_key_id=*********************)

[comment]: <> (aws_secret_access_key=*********************)

[comment]: <> (region=sa-east-1)

[comment]: <> (```)


[comment]: <> (To create the `venv` and install the modules execute:)

[comment]: <> (```)

[comment]: <> (./bin/venv.sh)

[comment]: <> (```)

[comment]: <> (If you don't want to create the venv, execute the follow commands:)

[comment]: <> (```)

[comment]: <> (./bin/install.sh)

[comment]: <> (./bin/install-vendor.sh)

[comment]: <> (```)

[comment]: <> (#### Running the chalice)

[comment]: <> (Execute the follow command:)

[comment]: <> (```)

[comment]: <> (./bin/chalice/run-local.sh)

[comment]: <> (```)

[comment]: <> (### Running via docker)

[comment]: <> (You will need the aws credentials for the profile `sigo-lambdas`:)

[comment]: <> (Create a copy of `docker/aws/credentials.example` to `docker/aws/credentials`;)

[comment]: <> (Edit the file with the credentiais.)

[comment]: <> (```)

[comment]: <> (cat ./docker/aws/credentials)

[comment]: <> ([sigo-lambdas])

[comment]: <> (aws_access_key_id=*********************)

[comment]: <> (aws_secret_access_key=*********************)

[comment]: <> (region=sa-east-1)

[comment]: <> (```)

[comment]: <> (To execute the build)

[comment]: <> (```)

[comment]: <> (./bin/runenv.sh --build)

[comment]: <> (```)

[comment]: <> (Execute the follow command:)

[comment]: <> (```)

[comment]: <> (./bin/runenv.sh)

[comment]: <> (```)

[comment]: <> (## Samples)

[comment]: <> (See the project samples in this folder [here]&#40;samples&#41;.)

[comment]: <> (## Running tests)

[comment]: <> (To run the unit tests of the project you can execute the follow command:)

[comment]: <> (First you need install the tests requirements:)

[comment]: <> ( ```)

[comment]: <> ( ./bin/venv-exec.sh ./bin/tests/install-tests.sh )

[comment]: <> ( ```)

 
[comment]: <> (### Unit tests:)

[comment]: <> ( ```)

[comment]: <> (./bin/venv-exec.sh ./bin/tests/unit-tests.sh)

[comment]: <> ( ``` )

[comment]: <> (### Functional tests:)

[comment]: <> (Executing the tests:)

[comment]: <> ( ```)

[comment]: <> (./bin/venv-exec.sh ./bin/tests/functional-tests.sh)

[comment]: <> (```)

[comment]: <> (### All tests: )

[comment]: <> (Executing the tests:)

[comment]: <> (```)

[comment]: <> ( ./bin/venv-exec.sh ./bin/tests/tests.sh )

[comment]: <> ( ```)

[comment]: <> (## Generating coverage reports)

[comment]: <> (To execute coverage tests you can execute the follow commands:)

[comment]: <> (Unit test coverage:)

[comment]: <> (``` )

[comment]: <> (./bin/venv-exec.sh ./bin/tests/unit-coverage.sh)

[comment]: <> (``` )

[comment]: <> (Functional test coverage:)

[comment]: <> (``` )

[comment]: <> (./bin/venv-exec.sh ./bin/tests/functional-coverage.sh)

[comment]: <> (``` )

[comment]: <> (> Observation:)

[comment]: <> (The result can be found in the folder `target/functional` and `target/unit`.)


[comment]: <> (## License)

[comment]: <> (See the license [LICENSE.md]&#40;LICENSE.md&#41;.)

[comment]: <> (## Contributions)

[comment]: <> (* Anderson de Oliveira Contreira [andersoncontreira]&#40;https://github.com/andersoncontreira&#41;)

[comment]: <> (* Allysson Santos [allyssonm]&#40;https://github.com/allyssonm&#41;)