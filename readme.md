# Pentatonica

A simple musical note sequencer with MIDI export support, designed to make music composition accessible to everyone.

![notes_svg](https://github.com/user-attachments/assets/edc7fb6d-6ae8-4892-8994-ec6a686e1639)

## What is the Pentatonic Scale?

The pentatonic scale is a five-note musical scale that has been used across cultures for thousands of years. Its beauty lies in its simplicity, because it omits the fourth and seventh scale degrees found in traditional major and minor scales, nearly any combination of its notes sounds harmonious together.

This makes the pentatonic scale incredibly beginner-friendly: you can play notes in almost any pattern or rhythm, and it will sound musically pleasing. There's no "wrong" note, making it perfect for experimentation and creative exploration. You can try playing with it even without knowing music theory.

## Features

- **Major and Minor Modes**: Pentatonica supports both major and minor pentatonic scales, use major for uplifting sounds or minor for more melancholic, soulful tones.

- **Easy Pattern Creation**: Create simple or complex musical patterns using an intuitive sequencer interface. Since the pentatonic scale is so forgiving, even random patterns can produce beautiful melodies.

- **MIDI Export**: Export your compositions as MIDI files to use in professional Digital Audio Workstations (DAWs), music production software, or share with other musicians. Your creative ideas can easily become full productions.

## Installation

### Prerequisites

- Python 3.x
- Required Python libraries:
  - `pygame`
  - `pyFluidSynth`
  - `mido`

Install the required libraries using pip:
```bash
pip install pygame pyFluidSynth mido
```

### Setup

1. Download the FluidR3_GM.sf2 soundfont (or a similar one) from [KeyMusician](https://member.keymusician.com/Member/FluidR3_GM/index.html)

2. Place the `FluidR3_GM.sf2` file in the `assets` folder of the project

3. Run the main file:
```bash
python main.py
```

## Licenses

This project is licensed under the **MIT license**.

## Contributing

Whether it's bug reports, feature suggestions, or code improvements, your help is appreciated.

### How to Contribute
1. **Fork the Repository**
   - Click the "Fork" button at the top right of this repository page to create your own copy.

2. **Create a New Branch**
   - Use a descriptive name for your branch:
     ```bash
     git checkout -b feature/your-feature-name
     ```

3. **Make Changes**
   - Add your code, fix bugs, or improve documentation.

4. **Commit Your Changes**
   - Provide a clear and concise commit message:
     ```bash
     git commit -m "Add your description here"
     ```

5. **Push to Your Branch**
   - Push the changes to your forked repository:
     ```bash
     git push origin feature/your-feature-name
     ```

6. **Open a Pull Request**
   - Go to the original repository and open a pull request from your branch.

### Guidelines
- Follow a standardized coding style.
- Include comments and documentation for new features.
- Make sure your code builds and runs without errors.
