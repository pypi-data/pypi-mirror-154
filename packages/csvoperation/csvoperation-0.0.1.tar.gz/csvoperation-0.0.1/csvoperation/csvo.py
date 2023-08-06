
class Readercsv:
    def __new__(self, file, separator='\n'):
        self.f = file
        self.s = separator
        return self.rt(self)

    def rt(self):
        return self.f.read().split(self.s)


class DictReadercsv:
    def __new__(self, file, separator='\n'):
        self.f = file
        self.s = separator
        return self.rt(self)

    def list2dict(self, lt, separator=','):
        dic = {}
        for x in lt.split(separator):
            dic[x] = ''
        return dic

    def rt(self):
        data = self.f.read().split(self.s)
        dic1 = self.list2dict(self, data[0])
        del data[0]
        data1 = data
        data = ','.join(data)
        z = 0
        lt = []
        y = 0
        dic = dic1.copy()
        for x in range(len(data1)):
            lt.append('')
            for z, i in enumerate(dic.keys()):
                dic[i] = data.split(',')[y]
                y += 1
                lt[x] = dic
            dic = dic1.copy()
        return lt


class Writercsv():
    def __init__(self, file, separator=','):
        self.f = file
        self.s = separator

    def writeRow(self, itera):
        self.f.write('\n')
        for x in range(len(itera)):
            self.f.write(str(itera[x]))
            if x != len(itera)-1:
                self.f.write(str(self.s))

    def writeRows(self, itera):
        for x in itera:
            self.writeRow(x)


class DictWritercsv(Writercsv):
    def __init__(self, file, title, separator=','):
        super()
        self.f = file
        self.s = separator
        self.t = title

    def titleWrite(self):
        self.writeRow(self.t)

    def DictWriteRow(self, dic):
        lt = []
        for i in self.t:
            lt.append(dic[i])
        self.writeRow(lt)

    def DictWriteRows(self, itera):
        for i in itera:
            self.DictWriteRow(i)
