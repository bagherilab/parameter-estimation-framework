# parameter-estimation-framework

Generalizable framework for parameter estimation with given objectives for ABMs. Parameter estimation algorithm is modular and can be replaced with any estimation algorithm. ABM input and output is expected to be in XML file format.

### framework outline
```
exit condition = objectives [regression in tumor size, avg tumor cell count < n]
loss_f = objective function based on exit conditions
model = whatever ML classifier 

while exit condition is not met:

    params_to_evaluate = next item in active_learning_outputs

    ### split the queue evaluation into n threads
    for each [parameter set] in params_to_evaluate:
        abm_outputs.add(run_java_abm([parameter set]))
    ### merge the threads 
    
    active_learning_outputs.add(active_learning_function(abm_outputs, loss_f, model))
```


### active learning outline
```

# takes in list of abm output values
# returns list of parameters for parameterization towards goal

def active_learning_function(abm_outputs, loss_f, model):
    obj_function = loss_f
    initial_parameters = random_sample(abm_outputs)
    unevaluated_params = abm_outputs
    evaluated_params = []

    loss = loss_f(initial_parameters)
    evaluated_params.add(initial_parameters)
    unevaluated_params.remove(initial_parameters)
    model.train(evaluated_params)

    while cross validation metric not satisfied in model and iterations < maximum iterations:
        probabilities = model.calculate_probabilities(unevaluated_params)
        clusters = k_means(probabilities)
        uncertain_points = all points in clusters w/ probability closest to 0.5
        random_points = random_sample(unevaluated_params - uncertain_points)
        loss = obj_function(uncertain_points, random_points)
        evaluated_params.add(uncertain_points, random_points)
        unevaluated_params.remove(uncertain_points, random_points)
        model.train(evaluated_params)

    return model.predict(unevaluated_points)

```

### run java abm outline
```
# takes in dictionary of parameters values and runs java abm program
# returns list of output values from abm

def run_java_abm(parameter_dict):

    xml_input_file = xml_encoder(parameter_dict)

    # call java program inside of python script
    xml_output_file = abm(xml_input_file)

    return xml_decoder(xml_output_file)

```

### xml encoder/decoder

```
# takes in dictionary of parameter:value sets
# returns xml file with parameter values

def xml encoder(parameter_dict):
    # some encoding according to expected file format
    # write to file
    return xml_file
```

```
# takes in xml file
# returns dictionary of abm output values

def xml encoder(xml_file):
    # some parsing according to file format
    # add to dictionary
    return output_dict
```