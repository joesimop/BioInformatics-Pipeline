import os
from parsing import load_stage_config
from helpers import pipeline_exists

class Pipeline:
    def __init__(self, pipeline_name):

        if not pipeline_exists(pipeline_name):
            raise ValueError(f"Pipeline {pipeline_name} does not exist")
        
        self.name = pipeline_name
        self.path = f"pipelines/{pipeline_name}"
        self.metadata_file = f"{self.path}/.{pipeline_name}_metadata.txt"
        self.stages = {}
        self.ordered_stages = []
        self.executions = []
        
    def add_stage(self, name, stage):
        self.stages[name] = stage
        
    def get_stage(self, stage_name):
        for stage in self.stages:
            if stage.name == stage_name:
                return stage
        return None
    
    def save_pipeline(self):
        with open(f"{self.path}/{self.name}.config", 'w') as file:
            file.write(f"Pipeline Name: {self.name}\n")
            file.write(f"Stages: {str([stage.name for stage in self.stages])[1:-1]}\n")
            file.close()
        
    # Loads the stages into the pipeline
    def load(self):
        stages = os.listdir(self.path)
        stages.remove("executions")
        for stage_name in stages:
            if os.path.isdir(f"{self.path}/{stage_name}"):
                self.add_stage(stage_name, load_stage_config(f"{self.path}/{stage_name}"))

    def verify_stage_compatablilty(self):
        for i in range(1, len(self.stages)):
            if self.stages[i].process.program.name not in self.stages[i-1].process.program.pipeline_stages:
                raise ValueError(f"Stage {self.stages[i].name} is not compatible with the previous stage")
            
    def sort_stages(self):
        
        # Find the initial stage, which does not depend on any other stages
        # Assumes only one such stage exists for simplicity
        initial_stage = next((stage for stage in self.stages if not stage.data_source_is_stage and stage.data_source == None), None)
        
        # If no initial stage with 'None', you might need to handle this case differently
        if not initial_stage:
            raise ValueError("No initial stage found or multiple initial stages exist.")

        # Build the ordered list of stages
        self.ordered_stages = [initial_stage]
        while True:

            last_stage = self.ordered_stages[-1]
            # Find the next stage whose data source is the name of the last stage
            next_stage = next((stage for stage in self.stages if stage.data_source_is_stage and stage.data_source == last_stage.name), None)
            
            if not next_stage:
                break  # No next stage found, sequence is complete
            
            self.ordered_stages.append(next_stage)


    def execute(self):

        #First, we need to update the run number in the metadata file
        with open(self.metadata_file, 'r+') as file:
            run_number = int(file.readline()[6])
            updated_run = f"runs: {run_number + 1}"
            file.seek(0)
            file.write(updated_run)
            file.close()


        output_dir = f"{self.path}/executions/run_{run_number}"
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)


        self.sort_stages()

        print("Executing Pipeline\n")
        last_ran_stage = None
        for stage in self.stages:


            #Make an output directory for the stage
            stage_output = f"{output_dir}/{stage.name}"
            if not os.path.exists(stage_output):
                os.mkdir(stage_output)
            
            #The input will exist, we checked when we loaded in the stages
            if stage.data_source_is_stage:
                input_dir = f"{output_dir}/{stage.data_source}/output"
            else:
                input_dir = f"data/{stage.data_source}"
                
            

            print(f"Executing Stage: {stage.name}")
            exec = stage.process.create_executable(input_dir, stage_output)
            print(f"Executing: {exec}")
            #os.system(exec)
        