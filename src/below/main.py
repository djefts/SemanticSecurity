import machine
import converter

if __name__ == "__main__":
    converter.readfromhub()
    machine.compare()
    machine.predict()
    machine.make_questions(20)