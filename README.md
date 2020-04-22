![LogoHub](https://logohub.appspot.com/Logo-Hub-36-white.png)

A Pornhub-Style Logo Service.

This project takes inspiration from [Shields IO](https://shields.io/).

# Example

* https://logohub.appspot.com/hello-world.png
* https://logohub.appspot.com/hello-world-30.webp

# Usage

Simply use URL as an image, which follows this this spec: 

```
<HostURL>/<Prefix>-<Suffix>[-FontSize][.Format]
```

> Component in `<>` means required, in `[]` means optional.

**Components:**

* HostURL: The root URL where the project be deployed.
* Prefix: Prefix text on the logo, can not be empty.
* Suffix: Suffix text on the logo, can not be empty.
* FontSize: Font size for prefix and suffix text, should be between 30 to 200, default is 60.
* Format: File format for the logo image, can be "png" or "webp", default is "png".

**Restriction:**

* `Prefix` and `Suffix` can not contain any of CJK characters.

# Deploy

Feel free to use the example service. 

But it is recommended to deploy this project to your own server, because the example service is under a free quota. 

**Google App Engine:**

```shell script
gcloud app deploy gae-app.yaml
```

**Heroku: TODO**

# TODO list

* Add parameter for setting logo background transparent.
* Add parameter for setting padding size around the logo.
* Support SVG format.

# License

MIT
