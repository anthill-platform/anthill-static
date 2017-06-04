## Upload a File

Uploads a File to a content delivery network, returning a static URL
for it for later use by the uploaded.

#### ← Request

```rest
PUT /upload
```

File body should be passed as `PUT` request contents, other arguments should be passed
as query arguments. The file will land on user's account folder.

| Argument         | Description                        |
|------------------|------------------------------------|
| `filename`       | Name of target file on CDN. If such file already exists on a target CDN, it will be overridden. |
| `access_token`   | A valid `AccessToken` with `static_upload` scope. |

#### → Response

In case of success, a JSON object with an URL for a newly placed file returned:
```json
{
    "url": "https://static-test.example.com/download/99/test.zip"
}
```

