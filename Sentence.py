class Sentence:

    def __init__(self, docId, sentId):
        self.patient_id = docId
        self.sentence_id = sentId
        self.sentence = []
        self.words = []
        self.lemma = []
        self.pos_tags = []
        self.ner_tags = []

    def array_to_str(self, array):
      arr_str = "{"
      for i in range(len(array)):
        arr_str += array[i]
        if (i < len(array) - 1):
          arr_str += ","
      arr_str += "}"
      return arr_str


    def to_string(self):
      return str(self.patient_id) + ", " + str(self.sentence_id) + "," + self.array_to_str(self.sentence) + "," + self.array_to_str(self.words) + "," + self.array_to_str(self.lemma) + "," + self.array_to_str(self.pos_tags) + "," + self.array_to_str(self.ner_tags)


