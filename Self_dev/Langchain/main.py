
from src.agents.pipeline import run_research_pipeline

user_info = {
    "Name": "John Doe",
    "Age": 30,
    "Gender": "Male",
    "Height": "5'10\"",
    "Weight": "80 kg",
    "Muscle to Fat Ratio": "15% Muscle, 25% Fat",
    "Fitness Goal": "Build Muscle and Reduce Fat",
    "Preferred Cuisine": "Indian-North Indian",
    "Dietary Restrictions": "Lactose Intolerant",
    "Sleep Patterns": "Average 6 hours of sleep per night",
    "Medical Conditions or Injuries": "None",
    "Lifestyle": "Sedentary job, active on weekends",
    "Motivation Level": "High"
}

User_info_str = "\n".join(f"{key}: {value}" for key, value in user_info.items())
run_research_pipeline(User_info_str)


