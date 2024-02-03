# captions-api-yt

FastAPI endpoint for the [youtube_transcript_api](https://pypi.org/project/youtube-transcript-api/) python package.

### Usage

#### `GET /transcript/{video_id}`

Example response:

```
{
    "transcript": "As soon as an aircraft is parked at the gate, several handlers and vehicles approach the aircraft from all directions. From cargo handlers and catering personnel to waste and fuel services, commercial aircraft ..."
}
```

#### `POST /summary`

Example request:

```
{
  "model": "sshleifer/distilbart-cnn-12-6",
  "text": "If you are like me then you go to the next thing to replace the thing that you burnt out and then you repeat. This video is not meant to scare you away from certain hobbies."
}
```

Example response:

```
{
    "success": true,
    "status": 200,
    "summary": [
        {
            "summary_text": "This video is not meant to scare you away from certain hobbies . If you are like me then [...]"
        }
    ]
}
```

Additionally the `min_length` parameter can be provided (along with `model` and `text`)` to override the default value.
