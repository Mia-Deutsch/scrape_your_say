import yaml

class DataHandler:
    def __init__(self, data: list[tuple[dict, dict, dict, dict]]) -> None:
        self.data: list[tuple[dict, dict, dict, dict]] = data
        self.prettify_file_names()
        self.remove_unknown_char()
        self.prettify_country_data()

    def get_title(self, box: dict) -> str:
        link: str = box["link"].split("/")[-1]
        title_splitted: list[str] = link.split("-")[1:-1]
        title: str = " ".join(title_splitted)
        return title

    def prettify_file_names(self) -> None:
        for index, item in enumerate(self.data):
            filename_list: list[tuple[str, str]] = []
            for name in item[1]["file_name"]:
                filename_list.append((name.split("-")[0][0:-1], name.split("\n")[0].split("-")[1][1::]))
            self.data[index][1]["file_name"] = filename_list

    def remove_unknown_char(self) -> None:
        deletable_keys: list[tuple[int, int, str, any]] = []
        for index, item in enumerate(self.data):
            try:
                for key, data in self.data[index][2]["by_country_respondent"].items():
                    if "ä" in key or "ö" in key or "ü" in key or "é" in key or "è" in key or "í" in key or "ì" in key:
                        deletable_keys.append((index, 2, key, data))
            except KeyError:
                pass

        for index, item in enumerate(self.data):
            try:
                for key, data in self.data[index][3]["by_country_respondent"].items():
                    if "ä" in key or "ö" in key or "ü" in key or "é" in key or "è" in key or "í" in key or "ì" in key:
                        deletable_keys.append((index, 3, key, data))
            except KeyError:
                pass

        for element in deletable_keys:
            key: str = element[2]
            new_key: str = key.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("é", "e").replace("è", "e").replace("í", "i").replace("ì", "i")
            self.data[element[0]][element[1]]["by_country_respondent"][new_key] = element[3]
            self.data[element[0]][element[1]]["by_country_respondent"].pop(element[2])

    def prettify_country_data(self) -> None:
        for index, item in enumerate(self.data):
            try:
                for key, data in self.data[index][2]["by_country_respondent"].items():
                    self.data[index][2]["by_country_respondent"][key] = int(data.split("(")[0])
            except KeyError:
                pass
            try:
                for key, data in self.data[index][3]["by_country_respondent"].items():
                    self.data[index][3]["by_country_respondent"][key] = int(data.split("(")[0])
            except KeyError:
                pass



    def prettify_data_yaml(self) -> list[dict]:
        yaml_data: list[dict] = []
        for index, item in enumerate(self.data):
            yaml_data.append({self.get_title(item[0]): {"main_page": item[0], "sub_page": item[1], "feedback_one": item[2], "feedback_two": item[3]}})
        return yaml_data

    def to_yaml(self) -> None:
        yaml_data: list[dict] = self.prettify_data_yaml()
        for data in yaml_data:
            with open("scraped_data.yaml", "a") as file:
                yaml.dump(data, file)