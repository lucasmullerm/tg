def getSongKey(filename):
    score = converter.parse(filename)
    key = score.analyze('key')
    scale = key.getScale()
    print('Scale:', scale.tonic.name)
    # print(key.tonic.name, key.mode)