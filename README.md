![LogoHub](https://logohub.appspot.com/Logo-Hub-36.svg?padding=0&scheme=white&transparent=true)

![](https://img.shields.io/badge/Release-v1.1.0-brightgreen?style=flat-square)
![](https://img.shields.io/badge/License-MIT-blue?style=flat-square)

A Pornhub-Style Logo Service.

This project takes inspiration from [Shields IO](https://shields.io/).

# Usage

Simply use a well-formed URL as an image, which follows this spec: 

```
<HostURL>/<Prefix>-<Suffix>[-FontSize][.Format][?Parameters]
```

> Component in `<>` means required, in `[]` means optional.

**Components:**

* HostURL: The root URL where the project be deployed.
* Prefix: Prefix text on the logo, can not be empty.
* Suffix: Suffix text on the logo, can not be empty.
* FontSize: Font size for prefix and suffix, in range of 30 to 200, default is 60.
* Format: Image file format, supports svg/png/webp, default is "svg".
* Parameters: QueryString-encoded optional parameters, see below for details.

**Parameters:**

* scheme: Color scheme of the logo, supports black/white, default is "black".
* transparent: Set background to transparent or not, default is "false".
* padding: Padding size around the logo, unset or negative will use a default size.

**Restriction:**

* `Prefix` and `Suffix` can not contain any of CJK characters.

# Example

* https://logohub.appspot.com/hello-world
* https://logohub.appspot.com/hello-world-90
* https://logohub.appspot.com/hello-world.png
* https://logohub.appspot.com/hello-world?transparent=true
* https://logohub.appspot.com/hello-world-120.webp?scheme=white&transparent=true&padding=0

# Deploy

Feel free to use the example service. 

But it is recommended to deploy this project to your own server, because the example service is under a free quota. 

**Google App Engine:**

```shell script
gcloud app deploy gae-app.yaml
```

**Heroku: TODO**

# License

MIT
