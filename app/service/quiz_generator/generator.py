from app.service.quiz_generator import verbs
from app.service.quiz_generator.common import QuizBuilder, Answer, Quiz

import random
import nltk

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger')
nltk.download('averaged_perceptron_tagger_eng')



class QuizGenerator:

    def __init__(self, quiz_builder: QuizBuilder) -> None:
        self.verb_tags = verbs.verb_tags
        self.builder = quiz_builder

    def generate_single_grammar(self, source: str, number_or_answers=4) -> Quiz:
        tokens = nltk.word_tokenize(source)
        pos_tags = nltk.pos_tag(tokens)

        verb_tags = [(idx, value) for idx, value in enumerate(
            pos_tags) if pos_tags[idx][1] in self.verb_tags]
        # print(verb_tags)

        extracted = random.choice(verb_tags)
        if (verbs.check_negative(extracted[0], pos_tags)):
            extracted, pos_tags = verbs.convert_verb_to_negative(
                extracted[0], pos_tags)

        pos_tags[extracted[0]] = ("_", extracted[1][1])

        new_answers = self.__generate_answers(number_or_answers, extracted[1])

        self.builder.create_question(pos_tags)
        self.builder.add_answer(Answer(text=extracted[1][0], is_correct=True))
        for a in new_answers:
            self.builder.add_answer(Answer(text=a, is_correct=False))
        quiz = self.builder.build()

        return quiz

    def generate_sequence(self, source: str):
        pass

    def generate_voice(self):
        pass

    def generate_context(self):
        pass

    def __generate_answers(self, number_of_answers: int, correct_answer: tuple) -> list[Answer]:

        correct_verb = correct_answer[0]
        correct_tense_tag = correct_answer[1]

        possible_tenses = self.verb_tags[:]  # fastest way to copy
        possible_tenses.remove(correct_tense_tag)

        new_tags = []
        new_verbs = []
        i = 1
        while i < number_of_answers and len(possible_tenses) > 0:
            tag = random.choice(possible_tenses)
            is_equal, new_verb = verbs.generate_tense_from_tag(
                tag, correct_verb)

            if not is_equal:
                new_tags.append(tag)
                new_verbs.append(new_verb)

            possible_tenses.remove(tag)
            i += 1

        return new_verbs


# g = QuizGenerator(QuizBuilder())
# t = "He worked hard from morning till night! And didn't know what joy it was."
# q = g.generate_single_grammar(t)
# print(q)

# print(json.dumps(q, default=lambda o: o.__dict__))