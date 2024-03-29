import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.ObjectNode;

import java.io.File;
import java.io.IOException;
import java.sql.SQLOutput;

public class JSONMethods {
    public boolean clearRequestedCourses(Student student) {

        try {
            // JSON file will be read
            File jsonFile = new File("src/Students/" + student.getStudentId() + ".json");

            // Read JSON data as follows
            ObjectMapper objectMapper = new ObjectMapper();
            JsonNode rootNode = objectMapper.readTree(jsonFile);

            // Find the "requestedCourses" field
            JsonNode requestedCoursesNode = rootNode.get("requestedCourses");

            // If the "requestedCourses" field is not empty, delete the content
            if (requestedCoursesNode != null && requestedCoursesNode.isArray()) {
                ArrayNode requestedCoursesArray = (ArrayNode) requestedCoursesNode;
                requestedCoursesArray.removeAll();
            }

            // Write changes to JSON file
            objectMapper.writeValue(jsonFile, rootNode);

        } catch (IOException e) {
            e.printStackTrace();
        }
        student.getRequestedCourses().clear();
        return true;
    }

    public boolean addEnrolledStudent(Student student, Course course) {
        try {
            File studentJsonFile = new File("src/Students/" + student.getStudentId() + ".json");
            ObjectMapper objectMapper = new ObjectMapper();
            JsonNode studentNode = objectMapper.readTree(studentJsonFile);

            JsonNode enrolledCoursesNode = studentNode.get("enrolledCourses");

            if (enrolledCoursesNode == null || !enrolledCoursesNode.isArray()) {
                enrolledCoursesNode = objectMapper.createArrayNode();
                ((ObjectNode) studentNode).set("enrolledCourses", enrolledCoursesNode);
            }

            ObjectNode newCourseNode = objectMapper.createObjectNode();
            newCourseNode.put("courseId", course.getCourseId());
            newCourseNode.put("courseName", course.getCourseName());
            newCourseNode.put("credit", course.getCredit());
            newCourseNode.put("prerequisite", course.hasPrerequisite());
            newCourseNode.put("prerequisiteLessonId", course.getPrerequisiteLessonId());

            ObjectNode courseSectionNode = objectMapper.createObjectNode();
            courseSectionNode.put("term", course.getCourseSection().getTerm());
            courseSectionNode.put("day", course.getCourseSection().getDay());
            courseSectionNode.put("hour", course.getCourseSection().getHour());
            courseSectionNode.put("status", course.getCourseSection().getStatus());
            courseSectionNode.put("semester", course.getCourseSection().getSemester());
            courseSectionNode.put("instructor", course.getCourseSection().getInstructor());
            courseSectionNode.put("enrollmentCapacity", course.getCourseSection().getEnrollmentCapacity());
            courseSectionNode.put("status", course.getCourseSection().getStatus());

            newCourseNode.set("courseSection", courseSectionNode);

            ((ArrayNode) enrolledCoursesNode).add(newCourseNode);

            objectMapper.writeValue(studentJsonFile, studentNode);

        } catch (IOException e) {
            e.printStackTrace();
        }
        return true;
    }

    public void addRequestCourse(Course course, Student student) throws IOException {

        try {
            File studentJsonFile = new File("src/Students/" + student.getStudentId() + ".json");
            ObjectMapper objectMapper = new ObjectMapper();
            JsonNode studentNode = objectMapper.readTree(studentJsonFile);

            JsonNode requestedCoursesNode = studentNode.get("requestedCourses");

            if (requestedCoursesNode == null || !requestedCoursesNode.isArray()) {
                requestedCoursesNode = objectMapper.createArrayNode();
                ((ObjectNode) studentNode).set("requestedCourses", requestedCoursesNode);
            }

            ObjectNode newCourseNode = objectMapper.createObjectNode();
            newCourseNode.put("courseId", course.getCourseId());
            newCourseNode.put("courseName", course.getCourseName());
            newCourseNode.put("credit", course.getCredit());
            newCourseNode.put("prerequisite", course.hasPrerequisite());
            newCourseNode.put("prerequisiteLessonId", course.getPrerequisiteLessonId());

            ObjectNode courseSectionNode = objectMapper.createObjectNode();
            courseSectionNode.put("term", course.getCourseSection().getTerm());
            courseSectionNode.put("day", course.getCourseSection().getDay());
            courseSectionNode.put("hour", course.getCourseSection().getHour());
            courseSectionNode.put("status", course.getCourseSection().getStatus());
            courseSectionNode.put("semester", course.getCourseSection().getSemester());
            courseSectionNode.put("instructor", course.getCourseSection().getInstructor());
            courseSectionNode.put("enrollmentCapacity", course.getCourseSection().getEnrollmentCapacity() - 1);
            courseSectionNode.put("status", course.getCourseSection().getStatus());

            newCourseNode.set("courseSection", courseSectionNode);

            ((ArrayNode) requestedCoursesNode).add(newCourseNode);

            objectMapper.writeValue(studentJsonFile, studentNode);

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void updateEnrollmentCapacity(String courseId, int newCapacity) throws IOException {
        File courseJsonFile = new File("src/course.json");
        ObjectMapper objectMapper = new ObjectMapper();
        JsonNode rootNode = objectMapper.readTree(courseJsonFile);

        JsonNode courseNode = findCourseNode(rootNode, courseId);

        if (courseNode != null) {
            ((ObjectNode) courseNode.get("courseSection")).put("enrollmentCapacity", newCapacity);

            objectMapper.writeValue(courseJsonFile, rootNode);
        } else {
        }


    }

    private JsonNode findCourseNode(JsonNode rootNode, String courseId) {
        if (rootNode != null && rootNode.isArray()) {
            for (JsonNode courseNode : rootNode) {
                if (courseNode.has("courseId") && courseNode.get("courseId").asText().equals(courseId)) {
                    return courseNode;
                }
            }
        }
        return null;
    }

    public void updateProjectAssistant(Student student, String projectAssistant) {
        try {
            File studentJsonFile = new File("src/Students/" + student.getStudentId() + ".json");
            ObjectMapper objectMapper = new ObjectMapper();
            JsonNode studentNode = objectMapper.readTree(studentJsonFile);

            ((ObjectNode)studentNode).put("projectAssistant", projectAssistant);

            objectMapper.writeValue(studentJsonFile, studentNode);

        } catch (JsonProcessingException e) {
            throw new RuntimeException(e);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

    }
}


