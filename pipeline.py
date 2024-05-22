import os
from parsing import load_stage_config
from helpers import pipeline_exists, byop_error, construct_file_extension_identifiers, contstruct_input_dir
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
        print(self.ordered_stages)
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
        stages = os.listdir(f"{self.path}/stages")
        for stage_name in stages:
            if os.path.isdir(f"{self.path}/stages/{stage_name}"):
                self.add_stage(stage_name, load_stage_config(f"{self.path}/stages/{stage_name}"))

        self.sort_stages()

    def verify_stage_compatablilty(self):
        for i in range(1, len(self.stages)):
            #If there in no intersection between the input file types of the current stage and the previous stage, error
            if not set(self.ordered_stages[i].process.program.input_file_types) & \
                set(self.ordered_stages[i-1].process.program.output_file_types):
                byop_error(f"Stage {self.ordered_stages[i-1].name} outputs {self.ordered_stages[i-1].process.program.output_file_types}\n" + \
                           f"\tStage {self.ordered_stages[i].name} requires {self.ordered_stages[i].process.program.input_file_types}")

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

        #First we need to veryify that the stages are compatible
        self.verify_stage_compatablilty()

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

        stage_output_dir = None

        print("Executing Pipeline\n")
        for stage in self.ordered_stages:

            # First, we need to construct the input directories for the stage
            # this will also verify that the input directories exist from the previous stage
            input_dir = contstruct_input_dir(stage, stage_output_dir)
            input_dir = construct_file_extension_identifiers(stage, input_dir)

            #Make an output directory for the stage
            stage_output_dir = f"{output_dir}/{stage.name}"
            if not os.path.exists(stage_output_dir):
                os.mkdir(stage_output_dir)

            print(f"Executing Stage: {stage.name}")
            exec = stage.process.create_executable(input_dir, stage_output_dir)
            print(f"Executing: {exec}")
            #os.system(exec)
        