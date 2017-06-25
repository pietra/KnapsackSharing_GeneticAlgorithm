# Genetic Algorithm

# Inicialize first population

# Calculate the fitness and volume of all chromosomes

# Check what percentage of the chromosomes in the population has the same fitness value
    # More than 90% ?
        # Yes:
            # 90% has the same fit value and the number of generations is greater than the limit?
                # Yes:
                    # STOP
                # No:
                    # Back to: "Calculate the fitness and volume of all chromosomes"
        # No:
            # Randomly select 2 chromosomes from the population
            # Perform crossover on the 2 chromosomes selected
            # Perform mutation on the chromosomes obtained


class GeneticAlgorithm:

    def __init__(self, seed):
        self.randomSeed = seed

    def calculating(self):
        print("MAIN DO CÁLCULO")

