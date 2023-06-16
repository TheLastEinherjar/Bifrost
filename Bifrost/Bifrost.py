from ..PuddingWebDriver.PuddingWebDriver import PuddingWebDriver
from selenium.webdriver.common.by import By
from . import bifrost_data_loader
import random
import os

class Bifrost :
    
    def __init__(self, pud_driver:PuddingWebDriver) -> None:
        self.path = str(os.path.dirname(__file__))
        self.pud_driver = pud_driver
        self.scripts = bifrost_scripts()

    def run_main(self) :
        self.daily_poll()
        self.this_or_that()
        self.clickables()
        self.turbocharge()
        self.test_your_smarts()

    def open_rewards_tab(self):
        def wait_for_tab(retries:int=5, cycle_time:int=5) :
            for _ in range(retries) :
                if self.pud_driver.find_element((By.ID, 'panelFlyout')) == None :
                    self.pud_driver.sleep(cycle_time)
                else :
                    self.pud_driver.sleep_range(4, 6)
                    return True
            return False
        # This may be a bit overkill
        while True :
            if self.pud_driver.find_element((By.ID, 'panelFlyout')) == None :
                if not self.pud_driver.is_element_visible((By.ID, "id_rh"), timeout=5) :
                    self.pud_driver.get("https://www.bing.com/")
                    self.pud_driver.sleep_range(10, 14)
                self.pud_driver.sleep_range(8, 10)
                if not self.pud_driver.click_element((By.ID, "id_rh"), timeout=20) :
                    print("selenium fail using java script")
                    self.pud_driver.execute_java_script("document.getElementById('id_rh').click();")

                if wait_for_tab(retries=10, cycle_time=2) :
                    continue
            else :
                self.pud_driver.sleep_range(4, 6)
                return
                

    def daily_poll(self) :
        pud_driver = self.pud_driver
        self.open_rewards_tab()
        if bool(pud_driver.execute_java_script(self.scripts.click_not_checked_elements(["Daily poll"]))) == True :
            self.pud_driver.sleep_range(15,20)

            random_value = random.randint(0,1)

            self.pud_driver.click_element((By.ID, f"btoption{random_value}"))
            self.pud_driver.sleep_range(5,8)

        pud_driver.sleep_range(2, 3)

    def clickables(self) :

        all_clickables = bifrost_data_loader.load_txt_lines(f'{self.path}/clickables.txt')
        pud_driver = self.pud_driver
        self.open_rewards_tab()
        pud_driver.sleep_range(6, 8)
        while bool(pud_driver.execute_java_script(self.scripts.click_not_checked_elements(all_clickables))) == True :
            pud_driver.sleep_range(15, 20)
            pud_driver.close_other_tabs(0)
            pud_driver.sleep_range(4, 6)
            self.open_rewards_tab()

        pud_driver.sleep_range(2, 3)

    def supersonic(self) :
        pud_driver = self.pud_driver
        self.open_rewards_tab()
        pud_driver.sleep_range(6, 8)
        if bool(pud_driver.execute_java_script(self.scripts.click_not_checked_elements(["Supersonic quiz"]))) == True :
            pud_driver.sleep_range(15, 20)
            pud_driver.click_element((By.ID, "rqStartQuiz"))
            pud_driver.sleep_range(5,10)
            for _ in range(3) :
                answers = pud_driver.execute_java_script(self.scripts.supersonic_answers)
                for answer in answers :
                    pud_driver.click_element((By.ID, str(answer)))
                    pud_driver.sleep_range(6,8)
                pud_driver.sleep_range(6,9)

            pud_driver.sleep_range(2, 3)

    def turbocharge(self) :
        pud_driver = self.pud_driver
        self.open_rewards_tab()
        pud_driver.sleep_range(6, 8)
        if bool(pud_driver.execute_java_script(self.scripts.click_not_checked_elements(["Turbocharge quiz"]))) == True :
            pud_driver.sleep_range(15, 20)
            pud_driver.click_element((By.ID, "rqStartQuiz"))
            pud_driver.sleep_range(5,10)
            for _ in range(3) :
                answer = pud_driver.execute_java_script(self.scripts.turbo_correct_id)
                pud_driver.click_element((By.ID, str(answer)))
                pud_driver.sleep_range(10,15)
            pud_driver.click_element((By.ID, "rqCloseBtn"), 10)

        pud_driver.sleep_range(2, 3)
        
    def test_your_smarts(self) :
        test_your_smarts_reskins = bifrost_data_loader.load_txt_lines(f'{self.path}/test_your_smarts_reskins.txt')
        pud_driver = self.pud_driver
        self.open_rewards_tab()
        pud_driver.sleep_range(6, 8)
        while bool(pud_driver.execute_java_script(self.scripts.click_not_checked_elements(test_your_smarts_reskins))) == True :
            pud_driver.sleep_range(8, 13)
            current_question = 0
            for _ in range(20) :
                pud_driver.sleep_range(6,8)
                answer_id = str(pud_driver.execute_java_script(self.scripts.test_your_smarts_correct_id))
                pud_driver.click_element((By.ID, answer_id))
                pud_driver.sleep_range(5,7)
                if pud_driver.get_attribute((By.XPATH, "//span[@class='cbtn']/input[@type='submit']"), 'value') == 'Get your score' :
                    pud_driver.sleep_range(1,2)
                    print(pud_driver.click_element((By.XPATH, "//span[@class='cbtn']/input[@type='submit']")))
                    break
                else :
                    pud_driver.click_element((By.XPATH, "//span[@class='cbtn']/input[@type='submit']"))
                    current_question += 1

            pud_driver.sleep_range(10,15)
            self.open_rewards_tab()

        pud_driver.sleep_range(2, 3)

    def this_or_that(self) :
        pud_driver = self.pud_driver
        self.open_rewards_tab()
        pud_driver.sleep_range(6, 8)
        if bool(pud_driver.execute_java_script(self.scripts.click_not_checked_elements(["This or That?"]))) == True :
            pud_driver.sleep_range(15, 20)
            pud_driver.click_element((By.ID, "rqStartQuiz"))
            pud_driver.sleep_range(9,17)
            for _ in range(10) :
                answer = pud_driver.execute_java_script(self.scripts.this_or_that_id())
                pud_driver.click_element((By.ID, answer), timeout=25)
                pud_driver.sleep_range(9,17)

                    
                        

class bifrost_scripts :
    def __init__(self) -> None:
        self.get_rewards_dict = '''
        // Initialize an empty dictionary
        var elementDict = {};

        // Iterate through the elements
        for (let i = 0; i < elements.length; i++) {
            // Get the element's text content
            var text = elements[i].textContent;

            // Add the element to the dictionary with the key being its text content
            elementDict[text] = elements[i];
        }

        return elementDict;
        '''
        self.supersonic_answers = '''
        // Select all elements with id starting with 'rqAnswerOption'
        var answerOptions = document.querySelectorAll('[id^="rqAnswerOption"]');

        // Get the correct element ids and return the results
        return Array.from(answerOptions)
            .filter(option => {
                var imgElement = option.querySelector('img[alt="Correct Image"], img[alt="Wrong Image"]');
                return imgElement && imgElement.getAttribute('alt') === 'Correct Image';
            })
            .map(option => option.id);
        '''
        self.test_your_smarts_correct_id = '''
        // Find all elements with the class 'wk_hideCompulsary'
        var correctOptions = document.getElementsByClassName('wk_hideCompulsary');

        // Loop through the correct options
        for (let option of correctOptions) {
            // Get the parent element (which has the ID you need)
            var parentElement = option.parentElement;
        }
        // Return the parent element's ID
        return parentElement.id;
        '''
        self.turbo_correct_id = '''
        var value = _w.rewardsQuizRenderInfo.correctAnswer;
        var element = document.querySelector(`[value="${value}"]`);
        return element.id;
        '''
    def this_or_that_id(self) :
        return '''
        function getAnswerCode(key, string) {
            let t = 0;
            for (let i = 0; i < string.length; i++) {
                t += string.charCodeAt(i);
            }
            t += parseInt(key.slice(-2), 16);
            return t.toString();
        };

        var answerEncodeKey = _G.IG;
        var answerOne = document.querySelector('#rqAnswerOption0');
        var answerTwo = document.querySelector('#rqAnswerOption1');
        var correctAnswerCode = _w.rewardsQuizRenderInfo.correctAnswer;
        if (getAnswerCode(answerEncodeKey, answerOne.getAttribute('data-option')) == correctAnswerCode) {
            return answerOne.id;
        }
        if (getAnswerCode(answerEncodeKey, answerTwo.getAttribute('data-option')) == correctAnswerCode) {
            return answerTwo.id;
        }
        '''

    def click_not_checked_elements(self, text_list) :
        return '''
        function clickElementByTextAndNotChecked(textList) {
            // Identify the iframe you want to switch to
            var iframe = document.getElementById('panelFlyout');

            // Switch to the iframe's content
            var iframeContent = iframe.contentWindow.document || iframe.contentDocument;

            // Get all elements with the "promo-title" class
            var elements = iframeContent.querySelectorAll('.promo-title');

            // Iterate through the elements and check if their text matches any string in the textList
            for (var element of elements) {
                for (var text of textList) {
                    // Check if the element contains the specific text and is not checked
                    if (element.textContent.includes(text) && !element.parentElement.parentElement.querySelector('.checkMark')) {

                        // Scroll the element into view
                        element.scrollIntoView();

                        // Click the element using JavaScript
                        element.click();

                        return 1;
                    }
                }
            }

            // Return false if none of the elements are matched
            return 0;
        }
        ''' + f'return clickElementByTextAndNotChecked({text_list});'

