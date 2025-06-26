import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import json
from langdetect import detect
from google.cloud import storage

def simple_summary(text, limit=100):
    words = text.split()
    return ' '.join(words[:limit])

class ProcessText(beam.DoFn):
    def process(self, element):
        text = element.decode("utf-8")  # Pub/Sub sends bytes
        try:
            lang = detect(text)
        except:
            lang = "unknown"

        summary = simple_summary(text)

        result = {
            "language": lang,
            "summary": summary
        }

        yield json.dumps(result)

def run():
    options = PipelineOptions(
        runner="DirectRunner"
    )

    with beam.Pipeline(options=options) as p:
        (p
         | "Read from PubSub" >> beam.io.ReadFromPubSub(subscription="projects/atlantean-stone-462107-f4/subscriptions/pdf-topic-sub")
         | "Process Text" >> beam.ParDo(ProcessText())
         | "Write to File" >> beam.io.WriteToText("output/summary", file_name_suffix=".json")
        )

if __name__ == "__main__":
    run()
