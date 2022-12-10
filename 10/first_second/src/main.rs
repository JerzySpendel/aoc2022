use std::fs;

enum Instruction{
    NOOP,
    ADD(i32),
}

struct InstructionStack {
    value: i32,
    current_instruction: Option<Instruction>,
    cycles: i32,
    instructions: Vec<Instruction>
}

impl InstructionStack {
    pub fn new(instructions: Vec<Instruction>) -> Self {
        Self { cycles: 0, value: 1, instructions, current_instruction: None }
    }

    pub fn cycle(&mut self) -> i32 {
        let to_return = self.value;
        if self.current_instruction.is_none() {
            self.current_instruction = self.instructions.pop();
            self.cycles = 0;
        }
    
        match self.current_instruction {
            Some(Instruction::NOOP) => self.current_instruction = None,
            Some(Instruction::ADD(value)) => {
                match self.cycles {
                    0 => self.cycles += 1,
                    1 => {
                        self.value += value;
                        self.current_instruction = None
                    }
                    _ => panic!("Shouldn't happen")
                };
            }
            None => panic!("Shouldn't hapend")
        };

        to_return
    }

    pub fn get_value(&self) -> i32 {
        self.value
    }

}

fn main() {
    let data = std::fs::read_to_string("../input").expect("Couldn't read the file");
    let mut instructions: Vec<Instruction> = vec![];
    for line in data.split('\n'){
        let mut instruction_iter = line.split(' ').take(2);
        let instruction = instruction_iter.next().unwrap();
        instructions.push(match instruction {
            "noop" => Instruction::NOOP,
            "addx" => {
                let value = instruction_iter.next().unwrap();
                Instruction::ADD(value.parse::<i32>().unwrap())
            }
            _ => panic!("Invalid value {}", instruction)
        })
    }

    instructions.reverse();
    let mut stack = InstructionStack::new(instructions);

    let snapshot_at = vec![20, 60, 100, 140, 180, 220];
    // let mut strenghts = vec![];

    // PART 1
    // for cycle_number in 1..=220 {
    //     let value = stack.cycle();
    //     if snapshot_at.contains(&cycle_number) {
    //         println!("{}", value * cycle_number);
    //         strenghts.push(value * cycle_number);
    //     }
    // }
    // println!("{}", strenghts.iter().sum::<i32>())

    // PART 2

    for row in 0..=5 {
        let mut row_string = String::with_capacity(100);

        for column in 0..=39 {
            let value = stack.cycle();
            let pixel = column;

            // println!("Current pixel pisition = {}, current value = {}", pixel, value);

            if (pixel - value).abs() <= 1{
                row_string.push('#');
            }
            else {
                row_string.push('.');
            }
        }

        println!("{}", row_string);
    }


}
