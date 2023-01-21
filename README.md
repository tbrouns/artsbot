# ArtsBot

Semantic search NLP model for [thuisarts.nl](thuisarts.nl)

Enter any (Dutch) search query and the best-matching entry from the thuisarts database is returned. 

## Example

Input queries:

    {
       "input":[
          {
             "text":"Ik heb hoofdpijn"
          },
          {
             "text":"Ik ben verkouden"
          }
       ]
    }


Output entries:

    {
       "output":[
          {
             "label":"Hoofdpijn kan door veel dingen komen. Zoals slecht slapen, veel cafe\u00efne of vaak pijnstillers nemen.\nAanvallen van hoofdpijn kunnen door migraine komen.\nMeestal is de oorzaak van hoofdpijn niet ernstig.\nSoms kunt u zelf iets doen aan de oorzaak.\nBij veel hoofdpijn kunt u af en toe een pijnstiller nemen, zoals \nparacetamol\n\nBel uw huisarts voor een afspraak als u vaak hoofdpijn heeft.\n"
          },
          {
             "label":"Bij verkoudheid zijn de slijmvliezen in uw neus en keel ontstoken.\nU kunt klachten krijgen als een verstopte neus, niezen, hoesten, keelpijn, heesheid en oorpijn. \nVerkoudheid ontstaat door een virus.\nSoms is corona de oorzaak van verkoudheid. Laat u testen op \ncorona\nMedicijnen zijn bij verkoudheid niet nodig.\nU kunt misschien neusdruppels of neusspray gebruiken.\n"
          }
       ]
    }

## Set-up

### Pull the git submodules:

    git submodule update --init --recursive

### Install depedencies:

    pip install -r requirements.txt

### Build the Docker image:

    docker build -t prediction_docker_image .

### Create the model:

If you run this for the first time, it needs to scrape the summaries as well.

    python3 save_model.py

### Run the server:

    docker run -it --gpus all -v $(pwd)/local_test/test_dir:/opt/ml -p 8080:8080 --rm prediction_docker_image 
    python3 serve

It can take some time before the server is up and running.

## Testing

After setting up the server, you can test (local) inference in a different terminal with:

    cd local_test
    bash predict.sh input.json

The JSON output will be printed to the terminal. You can change the queries in `input.json`.