class ServerResponse:
    def __init__(self, status: str, data=None):
        self.status = status
        self.data = data

    @staticmethod
    def infeasible():
        return {"status": 400, "message": "Infeasible"}

    def to_json(self):
        if self.status == "Infeasible":
            return self.infeasible()
        else:
            return {"status": 200, "message": "Success", "data": self.data}
        
