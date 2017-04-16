import string
import random


def uMap(value,istart,istop,ostart,ostop):
    return ostart+(ostop-ostart)*((value-istart)/(istop-istart))



class DNA:
    nudm = 0
    genes = []
    phrase = ''
    fitness = 0
    def __init__(self, num):
        self.nudm = num
        self.genes.extend([None]*self.nudm)

        for i in range(self.nudm):
            self.genes[i] = random.choice(string.ascii_letters+" "+string.punctuation+string.digits)


    def getPhrase(self):
        self.phrase = ''.join(self.genes)

        return self.phrase
    def fitnessF(self,target):
        score = 0
        for i in range(0,len(self.phrase)):
            if self.phrase[i]==target[i]:
                score+=1

        self.fitness = score/len(target)

    def crossover(self, partner):
        child = DNA(len(self.phrase))
        midpoint = random.randint(0,len(self.phrase))

        for i in range(0,len(self.phrase)):
            if i > midpoint:
                child.genes[i] = self.genes[i]
            else:
                child.genes[i] = partner.genes[i]

        return child

    def mutate(self,mutationRate):
        for i in range(0,len(self.phrase)):
            if random.random(0,1)<mutationRate:
                self.genes[i] = random.choice(string.ascii_letters+" "+string.punctuation+string.digits)



class Population:
    mutationRate = 0.0
    population = []
    matingPool = [DNA]*1
    target = ""
    generations = 0
    finished = False
    perfectScore = 0
    numb = 0

    def __init__(self, p,m,num):
        self.numb = num
        self.target = p
        self.mutationRate = m
        #self.population = [DNA() for i in range(self.numb)]
        for i in range(0,len(self.population)):
            self.population[i] = DNA(len(self.target))

        #calcFitness()
        #self.matingPool = [DNA() for i in range(2)]
        finished = False
        generations = 0
        perfectScore = 1

    def calcFitness(self):
        for i in range(0,len(self.population)):
            self.population[i].fitnessF(self.target)

    def naturalSelection(self):
        self.matingPool = []
        maxFitness = 0
        for i in range(0, len(self.population)):
            if(self.population[i].fitness>maxFitness):
                maxFitness = self.population[i].fitness

        for i in range(0, len(self.population)):
            fitness = uMap(self.population[i].fitness,0,maxFitness,0,1)
            n = int(fitness*100)
            for i in range(0,n):
                self.matingPool.append(self.population[i])

    def generate(self):
        for i in range(0, len(self.population)):
            a = int(random.random(len(self.matingPool)))
            b = int(random.random(len(self.matingPool)))
            partnerA = self.matingPool[a]
            partnerB = self.matingPool[b]
            child = partnerA.crossover(partnerB)
            child.mutate(self.mutationRate)
            self.population[i] = child
        self.generations += 1


    def getBest(self):
        worldrecord = 0.0
        index = 0
        for i in range(0, len(self.population)):
            if self.population[i].fitness>worldrecord:
                index = i
                worldrecord = self.population[i].fitness

            if worldrecord == self.perfectScore:
                self.finished = True
                return self.population[index].getPhrase()

    def finishedF(self):
        return self.finished

    def getGenerations(self):
        return self.generations
    def getAverageFitness(self):
        total = 0.0
        for i in range(0, len(self.population)):
            total += self.population[i].fitness

        return total



def man():
    target = "kaszanka"
    popmax = 150
    mutationRate = 0.01

    population = Population(target,mutationRate,popmax)

    while True:
        population.naturalSelection()
        population.generate()
        population.calcFitness()

        if(population.finishedF()):
            print("Done")
        print("Best = ",str(population.getBest()))


if __name__ == "__main__":
    man()