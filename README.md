# Using the `nbconvert` library and GitHub actions for automated, version-controlled Jupyter notebooks

This repository demonstrates the use of the python `nbconvert` library and GitHub actions to automate reporting in a Jupyter notebook. Version control in Jupyter notebooks can be challenging: notebook metadata and binary blobs make for difficult git diffs. With this approach, one notebook is used as a template and never executed, making changes to that template easy to review and interpret. The `nbconvert` library is then used to generate an executed version of the notebook from the template. This process can be automated with GitHub actions, which is useful for generating up-to-date reports based on frequently-updated data.


![nbconvert and github actions](https://user-images.githubusercontent.com/84750618/149984042-f8c36efa-83e9-43ef-ba9f-f30c1535202c.png)

# Using this Repository

Want to try this for yourself? All you need to do is fork the repository and set up the appropriate credentials. Credentials need to be updated on GitHub and in the .env file (if editing locally).

## GitHub Secrets

In the forked GitHub repository, navigate to settings -> secrets and click "New repository secret." The following secrets are needed for the GitHub actions workflow to run successfully:
- `BITIO_PG_STRING`: This allows access to the bit.io repo where cleaned/transformed data are loaded and queried. First, create an account on [bit.io](https://bit.io). Create a new repository (equivalent to a database schema) for this project. From the repository page, on the upper left, click the green "Connect" button. Copy the "PostgeSQL connection string" value and save it as `BITIO_PG_STRING` in secrets.
- `BITIO_REPO`: the name of the bit.io repository created in the above step. Note that this must be qualified with the username. For example, in [our version](https://bit.io/bitdotio/bls_quit_rate) of this project, the value for `BITIO_REPO` is `bitdotio/bls_quit_rate`.
- `BLS_API_KEY`: API key for downloading data from the Bureau of Labor Statistics. You can register for a key [here](https://data.bls.gov/registrationEngine/).
- `FRED_API_KEY`: API key for downloading recessions data from the St. Louis FRED website. You can register for a key [here](https://fredaccount.stlouisfed.org/login/secure/).

![image](https://user-images.githubusercontent.com/84750618/149990324-f37e73f6-5680-4120-ba86-59c1a4150490.png)


If you intend to edit the project locally or run the scripts outside of the context of the GitHub actions workflow, add the variables listed above to the `env_template` file and save it with the name `.env`.
