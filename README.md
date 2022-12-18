# spatial_epidemy_model
# Getting stated 
If you want to simulate this spatial model on your machine and play around with different paramenter settings. 
clone the repository onto your local machine 

`git clone https://github.com/ilgonhciz/spatial_epidemy_model.git`

Then navigate into the folder and do 

`pip install -r requirements.txt`

Now you are ready to run the code. 

In case you have VScode installed, you can simple open the project and press `Ctrl + F5` to run the program


# Default Parameters
```json
{
    "main": {
        "country": "CH",
        "outbreak": "ZUE",
        "outbreak_percentage": 0.0001,
        "iteration": 2000,
        "savefig": true
    },
    "data": {
        "cutoff_density": 0.0
    },
    "map": {
        "resolution": [
            800,
            400
        ],
        "plot_offset": 30000,
        "lockdown_condition_type":"d",
        "lockdown_threshhold": -1
    },
    "modelunit": {
        "cutoff_radius": 2,
        "delta": [
            0.00,
            0.000,
            0.000
        ],
        "gamma": 0.00002,
        "alpha": 0.005,
        "beta": 0.005,
        "epsilon":[0.0003, 0.0001],
        "k":0.02
    },
    "file": {
        "result_folder": "CH_Presentation/"
    }
}
```

## Result Cases
### CH: Simulated Country Switzerland, Initial Outbreak Point Zuerich (ZUE) 
```json
{
  "country": "CH",  
  "outbreak": "ZUE",
  "outbreak_percentage": 0.0001,
  "cutoff_radius": 2,
}
```
#### CH no vaccination no travel restriction
```json
{
    "lockdown_condition_type":"d",
    "lockdown_threshhold": -1,
    "delta": [
        0.000,
        0.000,
        0.000
    ],
}
```
![results_CH_default](https://user-images.githubusercontent.com/56004270/207874819-83198ead-50da-46bf-8b8d-0b3e0deb13a1.gif)


#### CH no vaccination but with travel restriction
```json
{
    "lockdown_condition_type":"d",
    "lockdown_threshhold": 100,
    "delta": [
        0.000,
        0.000,
        0.000
    ],
}
```
![results_CH_lockdown](https://user-images.githubusercontent.com/56004270/207874909-c7f199ba-025c-478b-b3c3-e6a1a7a4487c.gif)

#### CH both vaccination and travel restriction
```json
{
    "lockdown_condition_type":"d",
    "lockdown_threshhold": -1,
    "delta": [
        0.005,
        0.000,
        0.000
    ],
}
```
![results_CH_lockdown_vac](https://user-images.githubusercontent.com/56004270/207874971-1e2b5389-ca38-46df-a387-ce79fbc4400a.gif)

### USA: Simulated Country USA, Initial Outbreak Point Newark Liberty International Airport (EWR) 
```json
{
  "country": "USA",
  "outbreak": "EWR",
  "outbreak_percentage": 0.0001,
  "cutoff_radius": 2,
}
```

#### USA no vaccination no travel restriction
```json
{
    "lockdown_condition_type":"i",
    "lockdown_threshhold": -1,
    "delta": [
        0.000,
        0.000,
        0.000
    ],
}
```
![results_USA_default](https://user-images.githubusercontent.com/56004270/207875016-4e486c82-1e4f-477d-a519-4b979ac6b700.gif)

#### USA no vaccination but with travel restriction
```json
{
    "lockdown_condition_type":"i",
    "lockdown_threshhold": 100,
    "delta": [
        0.000,
        0.000,
        0.000
    ],
}
```
![results_USA_lockdown](https://user-images.githubusercontent.com/56004270/207875051-87b84813-b31d-4088-8664-94f0f1307a6f.gif)

#### USA both vaccination and travel restriction
```json
{
    "lockdown_condition_type":"i",
    "lockdown_threshhold": 100,
    "delta": [
        0.005,
        0.000,
        0.000
    ],
}
```
![results_USA_lockdown_vac](https://user-images.githubusercontent.com/56004270/207875119-099888dd-45c2-41fa-82d2-13126c0ec34e.gif)


## Useful Websites
* Transportation Graph of SBB: https://www.kaggle.com/code/kmader/simple-traverse-of-sbb-graph
* Population Data: https://hub.worldpop.org/geodata/listing?id=69
* Geo Data Visualization Methods: https://towardsdatascience.com/visualising-global-population-datasets-with-python-c87bcfc8c6a6
* Weekly Meetings: https://docs.google.com/document/d/1WjRgGYknTx_IZWcyx3EKL3kB5jwHo4zlZ83-HDmQUWw/edit
* Final report on overleaf: https://www.overleaf.com/4445946635gfzhqzqmvfmh
* Google folder with all references: https://drive.google.com/drive/folders/1pHr12b_hbOArYMnK83dygjF9ecZNYtw_
* Slides for presentation: https://docs.google.com/presentation/d/1utnxgHE8n9Cp_1ZQ76-Gh_GFNWxBf3sbgZiKmRR1g5Q/edit?usp=sharing
