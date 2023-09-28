import java.util.List;
import java.util.Map;
import java.util.PriorityQueue;
import java.util.Set;

public class Dijkstra {
    private record LabeledState ( Character state, int cost) {}

  private static final int INFTY = 10000;

    private final PriorityQueue<LabeledState> notDiscovered;

    public Dijkstra(Character initialstate; List<Character> states, Map<Character, Set<Character>> transitions) {
        this.notDiscovered = new PriorityQueue<>(states.stream().map(s -> new LabeledState(s, INFTY)).toList());
    }

    public


}