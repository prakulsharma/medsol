# MedSol
### A simple and efficient way to cross-check prescriptions

For patients taking multiple prescription medications for their various medical conditions, the possibility of drug interactions is high and may have adverse effects on the patients. Often patients are unaware of their own medications and may be taking different formulations of the same drug prescribed by different doctors.

The devastating results of such interactions were realised especially during the COVID-19 pandemic when, due to the shortage of medicines, errors made by overworked doctors and panic buying, people overlooked the adverse effects of mixing medicines, over-dosing and consuming self-prescribed medicines which led to deteriorated immunities. Consequently, many succumbed to illnesses like Black Fungus.

This project aims at identifying such interactions in medical prescriptions which eases the process of prescribing medicines and therefore, decreases the chances of health complications.

## Website
https://medsol.herokuapp.com/

## Future prospects
- Parameters to be included:
    - age, sex, weight
    - allergic reactions
    - medical history 
- Improved UI/UX
    - medicine name recommendations

## Virtual Environment Setup
-   Create virtual environment
    - For linux users:

            mkvirtualenv -p `which python3.6` medsol

    - For windows users:

            mkvirtualenv -p3.6 medsol


-   Install dependencies:       

        pip install -r requirements.txt --extra-index-url https://pypi.python.org/simple

