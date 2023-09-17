import java.util.*;

public class TwoStackQueue<E> implements Queue<E> {
  private Stack<E> inStack = new Stack<>();
  private Stack<E> outStack = new Stack<>();

  @Override
  public int size() {
    return inStack.size() + outStack.size();
  }

  @Override
  public boolean isEmpty() {
    return inStack.isEmpty() && outStack.isEmpty();
  }

  @Override
  public boolean contains(Object o) {
    return inStack.contains(o) || outStack.contains(o);
  }

  @Override
  public Iterator<E> iterator() {
    return new Iterator<E>() {
      private ListIterator<E> inStackIterator = inStack.listIterator(inStack.size() - 1);
      private Iterator<E> outStackIterator = outStack.iterator();

      private boolean isInInstack = true;

      @Override
      public boolean hasNext() {
        return (isInInstack && inStackIterator.hasPrevious())
                  || (outStackIterator.hasNext());
      }

      @Override
      public E next() {
        if (isInInstack && inStackIterator.hasPrevious()) {
          return inStackIterator.previous();
        } else if (!isInInstack) {
          if (outStackIterator.hasNext())
            return outStackIterator.next();
          else
            throw new NoSuchElementException;
        } else {
          // isInInstack but inStackIterator.hasPrevious() == false
          if (outStackIterator.hasNext()) {
            isInInstack = false;
            return outStackIterator.next();
          } else {
            throw new NoSuchElementException;
          }
        }
      }


      @Override
      public Object[] toArray() {
        Object[] array = new Object[inStack.size() + outStack.size()];

        // array order needs to be compatible with iterator order,
        // according to Java API
        int i = 0;
        for (Iterator<E> iter = iterator(); iter.hasNext(); i++)
          array[i] = iter.next();

        return array;
      }

      @Override
      public <T> T[] toArray(T[] ts) {
        T[] array = new T[inStack.size() + outStack.size()];

        // array order needs to be compatible with iterator order,
        // according to Java API
        int i = 0;
        for (Iterator<E> iter = iterator(); iter.hasNext(); i++)
          array[i] = (T) iter.next();

        return array;
      }

      @Override
      public boolean add(E e) {
        return inStack.add(e);
      }

      @Override
      public boolean remove(Object o) {

      }

      @Override
      public boolean containsAll(Collection<?> collection) {
        return false;
      }

      @Override
      public boolean addAll(Collection<? extends E> collection) {
        return false;
      }

      @Override
      public boolean removeAll(Collection<?> collection) {
        return false;
      }

      @Override
      public boolean retainAll(Collection<?> collection) {
        return false;
      }

      @Override
      public void clear() {

      }

      @Override
      public boolean offer(E e) {
        return false;
      }

      @Override
      public E remove() {
        return null;
      }

      @Override
      public E poll() {
        return null;
      }

      @Override
      public E element() {
        return null;
      }

      @Override
      public E peek() {
        return null;
      }
    }
