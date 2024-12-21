class MainPageBox:
    def __init__(self, link: str = "", topic: str = "", stage: list[str] = None, feedback_status: list[str] = None, type_of_act: str = "", feedback_period_from: str = "", feedback_period_to: str = ""):
        self.link = link
        self.topic = topic
        self.stage = [] if stage is None else stage
        self.feedback_status = [] if feedback_status is None else feedback_status
        self.type_of_act = type_of_act
        self.feedback_period_from = feedback_period_from
        self.feedback_period_to = feedback_period_to

    def set_box_parameters(self, link: str = None, topic: str = None, stage: list[str] = None, feedback_status: list[str] = None, type_of_act: str = None, feedback_period_from: str = None, feedback_period_to: str = None):
        self.link = link if link is not None else self.link
        self.topic = topic if topic is not None else self.topic
        self.stage = stage if stage is not None else self.stage
        self.feedback_status = feedback_status if feedback_status is not None else self.feedback_status
        self.type_of_act = type_of_act if type_of_act is not None else self.type_of_act
        self.feedback_period_from = feedback_period_from if feedback_period_from is not None else self.feedback_period_from
        self.feedback_period_to = feedback_period_to if feedback_period_to is not None else self.feedback_period_to

    def get_box_info(self) -> dict:
        box_dict: dict = {"link": self.link,
                          "topic": self.topic,
                          "stage": self.stage,
                          "feedback_status": self.feedback_status,
                          "type_of_act": self.type_of_act,
                          "feedback_period_from": self.feedback_period_from,
                          "feedback_period_to": self.feedback_period_to}
        return box_dict