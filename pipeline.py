import os
from parsing import load_stage_config
from helpers import pipeline_exists, byop_error
from environment_setup import user_root

class Pipeline:
    def __init__(self, pipeline_name):

        if not pipeline_exists(pipeline_name):
            byop_error(f"Pipeline {pipeline_name} does not exist")
        
        self.name = pipeline_name
        self.path = f"{user_root}/pipelines/{pipeline_name}"
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
    
    def print(self):
        print(f"\nPipeline Name: {self.name}\n")
        for i in range(0, len(self.ordered_stages)):
            print(f"\nStage {i+1}: ", end="")
            print(self.ordered_stages[i])
    
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

        self.sort_stages()

    def verify_stage_compatablilty(self):
        for i in range(1, len(self.stages)):
            if self.stages[i].process.program.name not in self.stages[i-1].process.program.pipeline_stages:
                raise ValueError(f"Stage {self.stages[i].name} is not compatible with the previous stage")

    #Might be the most horiffic sorter to ever exist, but sort the stages in the order they should be executed  
    def sort_stages(self):
        
        # Find the initial stage, which does not depend on any other stages
        # Assumes only one such stage exists for simplicity
        initial_stage = next((self.stages[stage] for stage in self.stages if not self.stages[stage].data_source_is_stage), None)
        
        if not initial_stage:
            byop_error("No initial stage with a data source in the data folder found")


        # Build the ordered list of stages
        self.ordered_stages = [initial_stage]
        while True:

            last_stage = self.ordered_stages[-1]
            # Find the next stage whose data source is the name of the last stage
            next_stage = next((self.stages[stage] for stage in self.stages if self.stages[stage].data_source_is_stage \
                               and self.stages[stage].data_source == last_stage.name), None)
            
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

        print("Executing Pipeline\n")
        for stage in self.ordered_stages:


            #Make an output directory for the stage
            stage_output = f"{output_dir}/{stage.name}"
            if not os.path.exists(stage_output):
                os.mkdir(stage_output)
            
            #The input will exist, we checked when we loaded in the stages
            if stage.data_source_is_stage:
                input_dir = f"{output_dir}/{stage.data_source}/output"
            else:
                input_dir = f"{user_root}/data/{stage.data_source}"
                
            

            print(f"Executing Stage: {stage.name}")
            exec = stage.process.create_executable(input_dir, stage_output)
            print(f"Executing: {exec}")
            #os.system(exec)
        