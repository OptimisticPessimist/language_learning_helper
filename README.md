# Add \<ruby\> tags
Demo  
![result](https://github.com/GuitarBuilderClass/add_ruby_tags/blob/master/doc/ruby.gif?raw=true)

## Moan
The \<ruby\> tags are troublesome, aren't these?  
If we want to write 『<ruby>漢字<rp>(</rp><rt>かんじ</rt><rp>)</rp></ruby>を<ruby>読む<rp>(</rp><rt>よ　</rt><rp>)</rp></ruby>。』, we have to write the following code:
```
<ruby>漢字<rp>(</rp><rt>かんじ</rt><rp>)</rp></ruby>を<ruby>読む<rp>(</rp><rt>よ　</rt><rp>)</rp></ruby>。
```
If you want to write a long long sentence, How many tags do we need?  
And, how long does it take to do that?


## Dependency
- python 3.7+

## Useage
First of all, comment out the settings `config/setting.py` other than those you want to use.

e.g., You chose "development" mode
```python
# MODE = "production"
MODE = "development"
# MODE = "test"
```
This causes `app.py` to read the settings in the `config/production.yaml` file.
Of course **you need to prepare the file with that name** in advance.
`config/sample.yaml` is prepared as a sample it.

To launch the app, enter the following command:
```bash
$ python app.py
```

This app is using the dictionary of MeCab with Janome.
*Sometimes I notice mistakes in reading between tags*.
Take care you use it.

## Licence
Licensed under Apache License 2.0 and uses the MeCab-IPADIC dictionary/statistical model.  
See LICENSE.txt and NOTICE.txt for license details.

## Gratitude
[janome by mocobeta](https://github.com/mocobeta/janome)   
[Prism: syntax highlight and add a copy to clipboard button](https://prismjs.com/)
