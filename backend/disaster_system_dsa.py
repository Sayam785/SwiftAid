from datetime import datetime
import heapq

class Volunteer:
    def __init__(self, vid, name, group):
        self.id = vid
        self.name = name
        self.group = group
        self.is_available = True
        self.assigned_to = None
        self.admin_message = None

class VolunteerNode:
    def __init__(self, volunteer):
        self.volunteer = volunteer
        self.next = None

class VolunteerLinkedList:
    def __init__(self):
        self.head = None
    
    def add_volunteer(self, volunteer):
        new_node = VolunteerNode(volunteer)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

class Disaster:
    _id_counter = 1
    def __init__(self, dtype, severity, is_emergency, volunteers_needed, supplies_needed, description, reported_by, location, report_photo):
        self.id = Disaster._id_counter
        Disaster._id_counter += 1
        self.type = dtype
        self.severity = int(severity)
        self.is_emergency = is_emergency
        self.volunteers_needed = int(volunteers_needed)
        self.supplies_needed = supplies_needed
        self.description = description
        self.reported_by = reported_by
        self.status = "Pending"
        self.timestamp = datetime.now()
        self.location = location
        self.report_photo = report_photo
        self.resolution_photo = None
        self.resolution_feedback = None
        self.assigned_volunteers = []
        self.updates = []

    @property
    def assignedCount(self):
        return len(self.assigned_volunteers)

    def get_priority_tuple(self):
        emergency_priority = 1 if self.is_emergency else 0
        time_priority = self.timestamp.timestamp()
        return (-emergency_priority, -self.severity, time_priority, self.id, self)

class VolunteerUpdate:
    def __init__(self, disaster_id, volunteer_id, priority, description, update_photo):
        self.disaster_id = disaster_id
        self.volunteer_id = volunteer_id
        self.priority = priority
        self.description = description
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.update_photo = update_photo
    
    def to_dict(self):
        return self.__dict__

class DisasterSystem:
    def __init__(self):
        self.disaster_queue = []
        self.volunteer_list = VolunteerLinkedList()
        self.volunteer_map = {}
        self.disaster_map = {}
        self.setup_initial_data()

    def setup_initial_data(self):
        groups = ["Medical", "NDRF", "Rescue", "Logistics", "Firefighting", "Search", "Transport", "Comms"]
        for i in range(101, 121):
            vid = f"v{i}"
            self._add_volunteer_to_system(vid, f"Personnel {i}", groups[i % len(groups)])

    def _add_volunteer_to_system(self, vid, name, group):
        v = Volunteer(vid, name, group)
        self.volunteer_list.add_volunteer(v)
        self.volunteer_map[vid] = v

    def report_disaster(self, dtype, severity, is_emergency, volunteers_needed, supplies_needed, description, reported_by, location, report_photo):
        d = Disaster(dtype, severity, is_emergency, volunteers_needed, supplies_needed, description, reported_by, location, report_photo)
        self.disaster_map[d.id] = d
        heapq.heappush(self.disaster_queue, d.get_priority_tuple())
        return d.id
    
    def add_volunteer_update(self, disaster_id, volunteer_id, priority, description, update_photo):
        d = self.disaster_map.get(disaster_id)
        if d:
            update = VolunteerUpdate(disaster_id, volunteer_id, priority, description, update_photo)
            d.updates.append(update)
            return True
        return False

    def get_all_disasters(self):
        disaster_objects = list(self.disaster_map.values())
        disaster_objects.sort(key=lambda d: (-d.is_emergency, -d.severity, d.timestamp), reverse=False)
        return [self.disaster_to_dict(d) for d in disaster_objects]

    def get_disasters_by_reporter(self, reporter_id):
        disasters = [
            self.disaster_to_dict(d)
            for d in self.disaster_map.values()
            if d.reported_by == reporter_id
        ]
        disasters.sort(key=lambda d: (-d['is_emergency'], -d['severity'], d['timestamp']), reverse=False)
        return disasters

    def delete_disaster(self, disaster_id, reporter_id):
        d = self.disaster_map.get(disaster_id)
        if not d:
            return False, "Disaster not found."
        if d.reported_by != reporter_id:
            return False, "Permission denied. Only the original reporter can delete this."
        if d.status != "Pending":
            return False, f"Deletion failed. Report status is '{d.status}' (Admin is already handling it)."
        del self.disaster_map[disaster_id]
        return True, f"Disaster ID {disaster_id} successfully deleted."

    def disaster_to_dict(self, d):
        priority_type = "Emergency" if d.is_emergency else "Normal"
        return {
            "id": d.id,
            "type": d.type,
            "severity": d.severity,
            "priority_type": priority_type,
            "is_emergency": d.is_emergency,
            "volunteers_needed": d.volunteers_needed,
            "assignedCount": d.assignedCount,
            "assigned_volunteers": d.assigned_volunteers,
            "supplies_needed": d.supplies_needed,
            "description": d.description,
            "status": d.status,
            "reported_by": d.reported_by,
            "timestamp": d.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "location": d.location,
            "report_photo": d.report_photo,
            "resolution_photo": d.resolution_photo,
            "resolution_feedback": d.resolution_feedback,
            "updates": [u.to_dict() for u in d.updates]
        }
    
    def volunteer_to_dict(self, v):
        return {
            "id": v.id,
            "name": v.name,
            "group": v.group,
            "is_available": v.is_available,
            "assigned_to": v.assigned_to,
            "admin_message": v.admin_message
        }

    def get_all_volunteers(self):
        vols_data = []
        current = self.volunteer_list.head
        while current:
            vols_data.append(self.volunteer_to_dict(current.volunteer))
            current = current.next
        return vols_data

    def set_admin_message(self, volunteer_id, message):
        v = self.volunteer_map.get(volunteer_id)
        if v:
            v.admin_message = message
            return True
        return False

    def assign_volunteer(self, disaster_id, volunteer_id, deployment_message):
        d = self.disaster_map.get(disaster_id)
        v = self.volunteer_map.get(volunteer_id)
        if d and v and v.is_available and d.assignedCount < d.volunteers_needed:
            d.assigned_volunteers.append(volunteer_id)
            d.status = "InProgress"
            v.is_available = False
            v.assigned_to = disaster_id
            v.admin_message = deployment_message
            return True
        return False
    
    def auto_assign_volunteers(self, disaster_id, deployment_message="Deployment initiated. Proceed with caution."):
        d = self.disaster_map.get(disaster_id)
        if not d:
            return False
        assigned_before = d.assignedCount
        current = self.volunteer_list.head
        while current:
            v = current.volunteer
            if d.assignedCount >= d.volunteers_needed:
                break
            if v.is_available:
                self.assign_volunteer(d.id, v.id, deployment_message)
            current = current.next
        return d.assignedCount > assigned_before
    
    def resolve_disaster(self, disaster_id, resolution_photo):
        d = self.disaster_map.get(disaster_id)
        if d and d.status != "Resolved":
            d.status = "Resolved"
            d.resolution_photo = resolution_photo
            for vid in d.assigned_volunteers:
                v = self.volunteer_map.get(vid)
                if v:
                    v.is_available = True
                    v.assigned_to = None
                    v.admin_message = None
            d.assigned_volunteers = []
            d.updates = []
            return True
        return False

SYSTEM = DisasterSystem()
