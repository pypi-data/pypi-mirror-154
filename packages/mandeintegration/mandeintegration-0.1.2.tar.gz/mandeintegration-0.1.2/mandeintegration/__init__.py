import os
from typing import Any, Dict, List, Tuple, Union
from time import sleep
from dataclasses import dataclass, field
from selenium.webdriver import Chrome, Safari, Firefox, Edge
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ChromeOptions, FirefoxOptions, EdgeOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from webdriver_manager.chrome import ChromeDriverManager

from mandeintegration.config import LOGIN_URL, __DIR__
from mandeintegration.config.selectors import BrowserSelector
from mandeintegration.config.types import ExpenditureReport, ExpenditureReportDetail, Project
from datetime import datetime


__version__ = '0.1.2'


@classmethod
class NotFoundError(Exception):
    pass


@dataclass
class MandEIntegration:
    """
        MandE Integration Module class.
    """
    browser: Union[Safari, Edge, Firefox, Chrome]
    email: str
    password: str
    options: Union[FirefoxOptions, ChromeOptions, SafariOptions, EdgeOptions] = field(default_factory=ChromeOptions)
    
    _TIMER_SLEEP: int =  field(default=3, repr=False, init=False)
    _LOGIN_URL: str = field(default=LOGIN_URL, repr=False, init=False)
    _HOMEPAGE_URL: str = field(default=os.getenv('USADF_GRANT_URL'), repr=False, init=False)
    _REPORT_SUMMARY_TOTAL_ITEM = 'Grand Total'
    _REPORT_STATUS_DRAFT = '0 Draft'
    
    
    def setup(self) -> None:
        """
            Setup the USADF Grants application.
        """
        
        print('#️⃣  Setting up...')
        self.browser = Chrome(ChromeDriverManager().install(), options=self.options)
        self.browser.maximize_window()
        self.browser.delete_all_cookies()
        
    @property
    def categories_list(self) -> List[str]:
        return ['Infrastructure', 'Equipment Purchases', 'Working Capital / Input', 'Training', 'Technical Assistance', 'Administrative Support']
    
    @property
    def report_detail_header(self) -> List[str]:
        return ['description', 'narrative', 'lc_total', 'usd_total', 'percent_by_category', 'unexpended_balance', 'current_spend_lc', 'spend_to_date', 'exch_rate']
    
    @property
    def report_summary_header(self) -> List[str]:
        return ['category', 'lc_total', 'usd_total', 'percent_by_category', 'current_spend', 'spend_to_date_lc', 'spend_to_date_usd']

    
    def login(self) -> None:
        """
            Login to the USADF Grants application.
        """
        
        self.setup()
        self.browser.get(self._LOGIN_URL)
            
        email_field = self.browser.find_element(By.CSS_SELECTOR, BrowserSelector.LOGIN_USERNAME)
        email_field.clear()
        email_field.send_keys(self.email)
        
        password_field = self.browser.find_element(By.CSS_SELECTOR, BrowserSelector.LOGIN_PASSWORD)
        password_field.clear()
        password_field.send_keys(self.password)
        
        self.browser.find_element(By.CSS_SELECTOR, BrowserSelector.LOGIN_SUBMIT_BUTTON).click()
        print('🔐 Logging in...')
        # sleep(self._TIMER_SLEEP + 3)
        print('🟢 Logged in!')
        
        
    def search_grant(self, code: str) -> Any:
        print('🔎 Searching grant...')
        menu_bar = self.browser.find_element(By.ID, BrowserSelector.GRANT_MENU_BAR)
        menu_bar.find_element(By.CSS_SELECTOR, BrowserSelector.GRANT_LIST_CSS_SELECTOR).click()
        self.browser.switch_to.frame('app_win')
        
        project_selection = self.browser.find_element(By.XPATH, BrowserSelector.GRANT_PROJECT_CODE.format(code))
        parent_selection = project_selection.find_element(By.XPATH, '..')
        print('🟢 Grant found!')
        return parent_selection
    
        
    def open_grant(self, code: str):
        """_summary_
        """
        print('Opening grant...')
        parent_selection = self.search_grant(code);
        self.browser.execute_script("arguments[0].scrollIntoView();", parent_selection)
        self.browser.execute_script("arguments[0].click();", parent_selection)
        print('🟢 Grant opened!')


    def open_reports(self, period_start: datetime, period_end: datetime, name: str = '') -> None:
        """_summary_

        Args:
            name (str): _description_
        """
        
        print('📊 Opening reports...')
        self.browser.switch_to.default_content()
        self.browser.switch_to.frame('app_win')
        self.browser.find_element(By.ID, 'sf_1039835_tb').click()
        self.browser.switch_to.frame('listframe')
        
        report = None
        
        report_table = self.browser.find_element(By.ID, 'table_1753')
        report_body = report_table.find_element(By.TAG_NAME, 'tbody')
        report_list = report_body.find_elements(By.TAG_NAME, 'tr')
        
        
        print('🔎 Searching report...')
        for report_item in report_list:
            start_p, end_p = self.get_report_by_period(report_item)
            if start_p == period_start and end_p == period_end:
                print('🟢 Report found!')
                report = report_item
                break
        
        if report is None:
            print(f"😞 Oops! Report for the period of {period_start.strftime('%m/%d/%Y')} to {period_end.strftime('%m/%d/%Y')} not found!")
            print('❗ Quitting...')
            exit(1)
        
        print('🔎 Checking report status...')
        
        if self.get_report_status(report) == 1:
            print(f"🆖 Report is already approved for the period of {period_start.strftime('%m/%d/%Y')} to {period_end.strftime('%m/%d/%Y')}!")
            print('❗ Quitting...')
            exit(1)
            
        print('🆗 Report is in draft...')
        
        self.browser.execute_script("arguments[0].click();", report)
        
        print('🟢 Reports opened!')


    def open_expenditure_report(self) -> None:
        """_summary_
        """
        
        print('📊 Opening expenditure report...')
        self.browser.switch_to.default_content()
        self.browser.switch_to.frame('app_win')
        
        # expenditure_report_item = 
        self.browser.find_element(By.ID, 'cf_1434655_tb').click()
        # sleep(2)
        
        self.browser.window_handles[0]
        
        self.browser.find_element(By.ID, 'xml_1434749').click()
        # sleep(self._TIMER_SLEEP)
        
        window_after = self.browser.window_handles[1]
        
        self.browser.switch_to.window(window_after)
        
        # sleep(self._TIMER_SLEEP)
        print('🟢 Expenditure report opened!')
        
    
    def format_project_data(self, project_data: Any) -> Project:
        """_summary_"""
        code = project_data[0].text
        country = project_data[1].text
        grant_type = project_data[2].text
        name = project_data[4].text
        status = project_data[10].text
        start_date = project_data[8].text
        end_date = project_data[9].text
        budget_total_amount = project_data[6].text
        
        def format_amount(amount: str) -> float:
            return float(amount.replace('$', '').replace(',', ''))
        
        def format_country(country: str) -> str:
            return "NE" if country.upper() == "NIGER" else "US"
        
        def format_date(date: str) -> datetime:
            return datetime.strptime(date, '%m/%d/%Y')
        
        project = Project(code, name, format_date(start_date), format_date(end_date), format_amount(budget_total_amount), status, grant_type, format_country(country))
        
        return project
    
    # GRANT DATA
    def get_grant_data(self, code: str) -> Project:
        """_summary_
        """
        parent_selection = self.search_grant(code);
        
        project_info_td = parent_selection.find_elements(By.TAG_NAME, 'td')
        project_data = project_info_td[2:13]
        
        return self.format_project_data(project_data)
        

    def get_report_row_data(self, report_row: Any) -> List[Any]:
        return report_row.find_elements(By.TAG_NAME, 'td')
    
    def get_report_status(self, report_row: Any) -> int:
        report_data = self.get_report_row_data(report_row)
        status = report_data[6].text
        
        if status.lower() in self._REPORT_STATUS_DRAFT.lower():
            return 0
        return 1
        

    def get_report_by_period(self, report_row: Any) -> Tuple[datetime, datetime]:
        report_data = self.get_report_row_data(report_row)
        report_period_start = datetime.strptime(report_data[3].text, '%m/%d/%Y')
        report_period_end = datetime.strptime(report_data[4].text, '%m/%d/%Y')
        
        return report_period_start, report_period_end


    # Report Summary Section
    def get_summary_report_container(self) -> Any:
        report_summary = self.browser.find_element(By.ID, 'headingDiv')
        return report_summary.find_element(By.CLASS_NAME, 'summaryDetails')
    
    
    def get_summary_report_table(self) -> Any:
        return self.get_summary_report_container().find_element(By.TAG_NAME, 'table')
    
    
    def get_summary_report_body(self) -> Any:
        return self.get_summary_report_table().find_element(By.TAG_NAME, 'tbody')

                
    def get_summary_report_row(self, row_index_start: int, row_index_stop: int = 0) -> Any:
        """_summary_
        """
        if row_index_stop == 0:
            return self.get_summary_report_body().find_elements(By.TAG_NAME, 'tr')[row_index_start:]
        return self.get_summary_report_body().find_elements(By.TAG_NAME, 'tr')[row_index_start:row_index_stop]

    # Report Detail Section
    
    def get_detail_report_body(self, content_wrapper: Any) -> Any:
        return content_wrapper.find_element(By.TAG_NAME, 'tbody')
    
    def get_detail_report_footer(self, content_wrapper: Any) -> Any:
        return content_wrapper.find_element(By.TAG_NAME, 'tfoot')
    
    def get_detail_report_body_row(self, content_wrapper: Any) -> Any:
        return self.get_detail_report_body(content_wrapper).find_elements(By.TAG_NAME, 'tr')
    
    def get_detail_report_footer_row(self, content_wrapper: Any) -> Any:
        return self.get_detail_report_footer(content_wrapper).find_elements(By.TAG_NAME, 'tr')[0]
    
    def add_report_body_content(self, row_data: Any) -> ExpenditureReportDetail:
        """_summary_
        """
        report = ExpenditureReportDetail(
                description=row_data[0].find_element(By.TAG_NAME, 'textarea').get_attribute('value'),
                narrative=row_data[1].find_element(By.TAG_NAME, 'textarea').get_attribute('value'),
                lc_total=row_data[2].find_element(By.TAG_NAME, 'input').get_attribute('value'),
                usd_total=row_data[3].find_element(By.TAG_NAME, 'input').get_attribute('value'),
                percent_by_category=row_data[4].find_element(By.TAG_NAME, 'input').get_attribute('value'),
                unexpended_balance=row_data[5].find_element(By.TAG_NAME, 'input').get_attribute('value'),
                current_spend_lc=row_data[6].find_element(By.TAG_NAME, 'input').get_attribute('value'),
                spend_to_date=row_data[7].find_element(By.TAG_NAME, 'input').get_attribute('value'),
                exch_rate=row_data[8].find_element(By.TAG_NAME, 'input').get_attribute('value'),
        )
        
        return report
    
    def add_report_footer_content(self, row_data) -> ExpenditureReportDetail:
        report_total = ExpenditureReportDetail(
            description=row_data[0].find_element(By.TAG_NAME, 'input').get_attribute('value'),
            narrative=row_data[1].find_element(By.TAG_NAME, 'input').get_attribute('value'),
            lc_total=row_data[2].find_element(By.TAG_NAME, 'input').get_attribute('value'),
            usd_total=row_data[3].find_element(By.TAG_NAME, 'input').get_attribute('value'),
            percent_by_category=row_data[4].find_element(By.TAG_NAME, 'input').get_attribute('value'),
            unexpended_balance=row_data[5].find_element(By.TAG_NAME, 'input').get_attribute('value'),
            current_spend_lc=row_data[6].find_element(By.TAG_NAME, 'input').get_attribute('value'),
            spend_to_date=row_data[7].find_element(By.TAG_NAME, 'input').get_attribute('value'),
            exch_rate=row_data[8].find_element(By.TAG_NAME, 'input').get_attribute('value'),
        )
        
        return report_total
    
    def add_report_summary_content(self, row_data) -> ExpenditureReport:
        report = ExpenditureReport(
                category=row_data[0].text,
                lc_total=row_data[1].find_element(By.TAG_NAME, 'input').get_attribute('value'),
                usd_total=row_data[2].find_element(By.TAG_NAME, 'input').get_attribute('value'),
                percent_by_category=row_data[3].find_element(By.TAG_NAME, 'input').get_attribute('value'),
                current_spend=row_data[4].find_element(By.TAG_NAME, 'input').get_attribute('value'),
                spend_to_date_lc=row_data[5].find_element(By.TAG_NAME, 'input').get_attribute('value'),
                spend_to_date_usd=row_data[6].find_element(By.TAG_NAME, 'input').get_attribute('value'),
            )
        
        return report
        
    
    def retrieve_expenditure_report_content(self, code: str) -> List[ExpenditureReport]:
        """_summary_
        """
        print('🗃️  Retrieving expenditure report content...')
        reports: List[ExpenditureReport] = []
        report_row = self.get_summary_report_row(1)
        
        for row in report_row:
            row_data = row.find_elements(By.TAG_NAME, 'td')[1:]
            report = self.add_report_summary_content(row_data)
            reports.append(report)
        
        print('🟢 Expenditure report content retrieved!')
        return reports        
    
    def retrieve_expenditure_report_detail(self, code: str, category: str) -> List[ExpenditureReportDetail]:
        """_summary_
        """
        reports: List[ExpenditureReportDetail] = []     
        category_content = self.get_category_content(category)
            
        if category_content is None:
            raise NotFoundError('Category not found')
        
        category_content_body_row = self.get_detail_report_body_row(category_content)
        category_content_footer_row = self.get_detail_report_footer_row(category_content)
        
        for row in category_content_body_row:
            row_data = row.find_elements(By.TAG_NAME, 'td')[1:]
            report = self.add_report_content(row_data)
            reports.append(report)
            
        row_data_total = category_content_footer_row.find_elements(By.TAG_NAME, 'td')
        report_total = self.add_report_footer_content(row_data_total)
        reports.append(report_total)

        return reports
    
    
    # Edit summary report for all category
    def edit_summary_report(self, category: str, category_value: str, exch_rate: str) -> None:
        print(f"📩 Defined summary report for <{category}> category")
        total_value_usd = 0
        report_row = self.get_summary_report_row(1, -2)
                
        for row in report_row:
            row_data = row.find_elements(By.TAG_NAME, 'td')[1:]
            category_text = row_data[0].text
            
            if  category.lower() in category_text.lower() and self._REPORT_SUMMARY_TOTAL_ITEM not in category_text.lower():
                category_report_summary_spend_to_date_lc = row_data[5].find_element(By.TAG_NAME, 'input')
                category_report_summary_spend_to_date_lc.clear()
                category_report_summary_spend_to_date_lc.send_keys(category_value.format('{:.2f}'))
                
                total_value_usd = float(category_value) / float(exch_rate.replace(',', ''))
                category_report_summary_spend_to_date_usd = row_data[6].find_element(By.TAG_NAME, 'input')
                category_report_summary_spend_to_date_usd.clear()
                category_report_summary_spend_to_date_usd.send_keys(str(total_value_usd).format('{:.2f}'))
                break
        
        print(f"🟢 Summary report for <{category}> category edited")
        
    
    # Set category details values
    def set_category_value(self, category_content: Any, values: List[Dict[str, str]]) -> Tuple[str, str]:
        total_lc, rate = 0, 1
        category_content_body = category_content.find_element(By.TAG_NAME, 'tbody')
        category_content_body_tr = category_content_body.find_elements(By.TAG_NAME, 'tr')
        
        for row in category_content_body_tr:
            row_data = row.find_elements(By.TAG_NAME, 'td')[1:]
            category_text = row_data[0].find_element(By.TAG_NAME, 'textarea').get_attribute('value')
            rate = row_data[8].find_element(By.TAG_NAME, 'input').get_attribute('value')
        
            for value in values:
                if value['description'].lower() in category_text.lower():
                    row_data[6].find_element(By.TAG_NAME, 'input').clear()
                    row_data[6].find_element(By.TAG_NAME, 'input').send_keys(value['current_spend_lc'])
                    
                    row_data[7].find_element(By.TAG_NAME, 'input').clear()
                    row_data[7].find_element(By.TAG_NAME, 'input').send_keys(value['spend_to_date'])
                    
                    total_lc += float(value['spend_to_date'].replace(',', ''))
        
        return str(total_lc), rate
        
    
    # Get category content
    def get_category_content(self, category: str) -> Union[Any, None]:
        categories = self.browser.find_elements(By.CLASS_NAME, 'headerTable')
        category_content = None

        for cat in categories:
            category_name = cat.find_element(By.TAG_NAME, 'h3').text
            if category.lower() in category_name.lower():
                category_content = self.browser.execute_script("""return arguments[0].nextElementSibling""", cat)
                break
        
        return category_content


    # Set summary report total value
    def set_summary_report_total_value(self):
        """_summary_
        """
        
        total_spend_to_date_lc = 0
        total_spend_to_date_usd = 0
        
        report_row = self.get_summary_report_row(1)
        for row in report_row:
            row_data = row.find_elements(By.TAG_NAME, 'td')[1:]
            
            if self._REPORT_SUMMARY_TOTAL_ITEM not in row_data[0].text:
                total_spend_to_date_lc += float(row_data[5].find_element(By.TAG_NAME, 'input').get_attribute('value').replace(',', ''))
                total_spend_to_date_usd += float(row_data[6].find_element(By.TAG_NAME, 'input').get_attribute('value').replace('$', '').replace(',', ''))
            
        total_row = report_row[-1].find_elements(By.TAG_NAME, 'td')[1:]
        total_row_lc = total_row[5].find_element(By.TAG_NAME, 'input')
        total_row_usd= total_row[6].find_element(By.TAG_NAME, 'input')
        
        total_row_lc.clear()
        total_row_lc.send_keys(str(total_spend_to_date_lc))
        
        total_row_usd.clear()
        total_row_usd.send_keys(str(total_spend_to_date_usd))
            
            
                


    # Edit grant report values
    def edit_report(self, category_list: List[str], values: List[Dict[str, str]]) -> None:
        """_summary_
        """
        for category in category_list:
            category_content = self.get_category_content(category)
            
            if category_content is None:
                raise NotFoundError('Category not found')
            
            summary_value, rate = self.set_category_value(category_content, values[category.lower()])
            self.edit_summary_report(category, summary_value, rate)
            
        self.set_summary_report_total_value()
        self.save_change()
        print("🎉 Report edited 🎉")
    

        
     # Save all changes
    def save_change(self) -> None:
        footer_actions = self.browser.find_element(By.ID, 'v-footer')
        footer_actions.find_element(By.ID, 'cmd_save').click()
        

